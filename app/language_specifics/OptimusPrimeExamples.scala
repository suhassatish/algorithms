/* Goal:
1. read the columns from a csv into a dataframe as type PickList
2. use TestFeatureBuilder to create Feature[PickList]s from this dataframe
3. call methods such as pivot() on these Feature[PickList] references from there
*/
case class Person(name: String, age: Int)
val name = FeatureBuilder.Text[Person].extract(_.name.toText).asPredictor
val age = FeatureBuilder.Text[Integral].extract(_.age.toIntegral).asPredictor
val reader = DataReaders.Simple.csvCase[Person])()

//if you dont know the type, use a GenericRecord
val name = FeatureBuilder.Text[GenericRecord].extract(_.getString("name").toText).asPredictor
val age = FeatureBuilder.Text[GenericRecord].extract(_.getInt("age").toIntegral).asPredictor
val reader = DataReaders.Simple.csv[GenericRecord]()
//optimus prime library user does not need to construct the data frame themselves
// if they define the features and use a CSV reader the workflow will make the dataframe for them
