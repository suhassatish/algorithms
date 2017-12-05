package com.krux.marketer.common

import com.krux.datapipeline.database.ReportsRedshift
import com.krux.datapipeline.datasource.DataNodeConversions._
import com.krux.datapipeline.tags.{Client, Owner, Tags}
import com.krux.datasource.spark.SparkDataSourceConfigured
import com.krux.datasource.sql.SqlDataSourceConfigured
import com.krux.hyperion.Implicits._
import com.krux.hyperion.activity._
import com.krux.hyperion.datanode.{RedshiftDataNode, S3DataNode}
import com.krux.hyperion.expression.Format
import com.krux.hyperion.resource.Ec2Resource
import com.krux.hyperion.workflow.{WorkflowExpression, WorkflowNoActivityExpression}
import com.krux.hyperion.{HyperionCli, activity}
import com.krux.marketer.datasource._

/**
  * Upload Marketing Performance data into redshift
  */
trait AbstractMPSegmentRedshiftLoaderPipeline
  extends MPDataPipelineDef
    with HyperionCli
    with SqlDataSourceConfigured
    with SparkDataSourceConfigured {

  def source: MPSource.Value
  def name: String
  def numBaseBatches: Int // num of base org batches, range 0 to (numBaseBatches - 1)
  def startSpecialBatches: Int  // start index for special org batches - orgs that require special treatment
  def numSpecialBatches: Int    // num special batches

  override def track: Tags = Tags(Owner.OrangeTeam, Client.All, name).feature("MarketerPerformance")

  def day: String = Format(SparkActivity.ScheduledStartTime - 1.day, "yyyy-MM-dd")

  def batchIds: Seq[Int] = Seq.range(0, numBaseBatches) ++ Seq.range(startSpecialBatches, startSpecialBatches + numSpecialBatches)

  override def workflow = {

    val ec2 = Ec2Resource()

    /* Since some batches are frequently failing (DEV-8295), we dont want to wait on all S3 `_SUCCESS` objects,
     for 6 hours before starting. Instead, we want to load whatever batches exist after 6 hours. This way, we atleast
     load data for most orgs rather than not loading any at all when a handful of org_ids in just 1 batch fail.*/

    val copyActivities = {
      val tablePrimaryKeysS3Location: Seq[Seq[(String, List[String], S3DataNode)]] = {
        batchIds
          .map { batchId =>
            Seq(
              (
                "t_bf_adidas_07_17_mp_segment_data",
                List("organization_uuid", "day", "channel", "segment_uid"),
                MPSegmentDS.MPKeyedSegmentDS(source, day, s"batch-$batchId"): S3DataNode
              ),
              (
                "t_bf_adidas_07_17_mp_campaign_segment_data",
                List("organization_uuid", "day", "channel", "campaign_uid", "segment_uid"),
                MPCampaignSegmentDS.MPKeyedCampaignSegmentDS(source, day, s"batch-$batchId"): S3DataNode
              ),
              (
                "t_bf_adidas_07_17_mp_campaign_ad_segment_data",
                List("organization_uuid", "day", "channel", "campaign_uid", "ad_uid", "segment_uid"),
                MPCampaignAdSegmentDS.MPKeyedCampaignAdSegmentDS(source, day, s"batch-$batchId"): S3DataNode
              ),
              (
                "t_bf_adidas_07_17_mp_campaign_placement_segment_data",
                List("organization_uuid", "day", "channel", "campaign_uid", "placement_uid", "segment_uid"),
                MPCampaignPlacementSegmentDS.MPKeyedCampaignPlacementSegmentDS(source, day, s"batch-$batchId"): S3DataNode
              ),
              (
                "t_bf_adidas_07_17_mp_site_segment_data",
                List("organization_uuid", "day", "channel", "site_uid", "segment_uid"),
                MPSiteSegmentDS.MarketingPerformanceKeyedSiteSegmentDS(source, day, s"batch-$batchId"): S3DataNode
              )
            )
          }
      }

      tablePrimaryKeysS3Location
        .map { batchTables =>
          batchTables
            .map { case (table, primaryKeys, s3Location) =>

              val destTable = RedshiftDataNode(ReportsRedshift, table)
                .withSchema("public")
                .withPrimaryKeys(primaryKeys: _*)

              RedshiftCopyActivity(
                input = s3Location,
                output = destTable,
                insertMode = RedshiftCopyActivity.Append
              )(ec2)
                .named(s"upload_${table}_ToRedshift")
                .withCommandOptions(RedshiftCopyOption.gzip, RedshiftCopyOption.delimiter("^"))
                .withMaximumRetries(0)

            }
            .foldLeft[WorkflowExpression](WorkflowNoActivityExpression)(_ ~> _)
        }
        .foldLeft[WorkflowExpression](WorkflowNoActivityExpression)(_ + _)
    }

    copyActivities ~>
      activity
        .ShellCommandActivity("echo SUCCESS")(ec2)
        .onFail(getPipelineAlarm(s"[$name] Redshift Loader Failed"))
  }

}

