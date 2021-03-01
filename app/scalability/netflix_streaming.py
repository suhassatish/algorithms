"""
Design a content streaming product like Netflix.
Should be able to stream different types of content simultaneously across millions of different types of device
platforms with different network conditions (3G/4G/wifi).

Aspects to think about: content ingestion, data serving, real time playback with QOS management.

************************************************************************************************

Reading pointers:
https://techtakshila.com/system-design-interview/chapter-2/

Capacity planning:
1) Assume on avg 1 movie size is 2.5 GB, 200M monthly active users, 10K connections per server, 20 ms service latency
Avg user streams 3 movies per day and daily active users at peak traffic are 75% of them using the playback service.

0.75 * 200M users * 20 ms / 10K cnxns = 300 servers
----
API interface design

video upload service
POST video-content/v1/videos
body {
    title: "<TITLE>"
    description: "description of video"
    tags: "List<Tags>" # genre
    type: "docu series, show"
    video stream:
}

search video service
GET /video-content/v1/search
query params {
    geo
    device-type
}

stream video service
GET /video-content/v1/videos/
query params {
    video_id
    offset: "second where video is paused for this particular user profile"
}


************************************************************************************************
https://www.slideshare.net/adrianco/netflix-global-cloud
Infra presentation by Adrian Cockcroft

Highlights:
1) Separate API endpoints per device
2) Transcoding for those devices
3) DRM licensing for content creators
4) gRPC based on HTTP/2 for inter-service communication using protobufs - compact, schema versioning is there,
bidirectional streaming and flow control capabilities of HTTP/2 come for free.

-----------------
A) how to detect low bandwidth and switch to lower resolution video? Ans: https://preseem.com/2018/04/netflix-behavior-wireless-network/
hashed movieId to manifestFile for this video  that contains the  different files encoded in different bit rates and
different resolutions that the device being used can play.

    Client-side buffer requests video file chunks from CDNs and tries to keep the buffer full.

    If the app is unable to keep the buffer full, it’ll switch to a lower resolution video and start a new buffer, and
    then sometime after that, the bitrate it’s actually playing will switch down to that lower resolution/lower quality.

6) Captions for a movie can be stored in openTSDB, a timeseries database with the movie timelines.

7) Netflix videos are variable bitrate encoded (and dependent on genre of movie amongst other things) therefore it’s not
possible to limit resolution (like standard def) with network policy.

8) Netflix downloads in short bursts at full link rate, which can negatively impact other traffic like gaming packets or
 VoIP. A strategy to fix QoE problems associated with Netflix behavior is to leverage modern queuing technologies such
 as FQ-CoDel.
-----------------


************************************************************************************************
IK mock interview feedback -

5 mins intro.

45 mins technical

rest is feedback.

design netflix-like system - movie streaming service. focus on playing movies specifically - starts from the moment the movie is selected.
search, rec sys, browsing catalog.

play movie. clients could be tv, mobile device, browser window. adapt movie quality to B/W of N/W connection.
congested. streaming gets adapted to available bandwidth - increasing compression fluent playback.

10M movies a day. geographic time zones, even immediately.
latencies - sub-second. 10s.
movies - 1 M movies.

----------

client - context -

;

caching proxy ;
authentication ;

turn off the tv , open the movie in night.
cross device compatibility

----

of all the movies that were played, upto what point they have seen.

----
feedback -

https://uplevel.interviewkickstart.com/interview/814/
Document the API, including input and output schema, auth tokens, pagination tokens * Document the data model for every
data store, queue, cache, include partition, retention, eviction and replication policies (include all these in the
cost) * Evaluate scalability and bottlenecks, include bandwidth, and handling popular items (orchestration to provision
resources) * Try to document in the whiteboard all the relevant details that described verbally

organization on editor - could be improved
v structured, intentionally organized presentation of spec
aspects, history, movie.
things will explain how it works is in this spec.

what to improve?
no detail on API the client sees. Q & A. rest JSON API. input and output of history service.
movie server. more detail - could be the crux of the interview.
data model - this is discrete determined. which data stores we have. cache , queue, DB, KV store.
schema definition has a type - list, map, complex type. those are explained a little bit more.

scaling part.
replication  part tricky. can have movies that are v.popular.
orchestration that replicates copies of that movie.

growth of data. new history entries everyday . back of the envelope for growth factor of data store.
provision new nodes to accommodate.
playing and pausing - detecting those events. also account for anything. turn off the tv or lost power.
switched to another device. overall - security of the content. studios are v.protective of their content.

cdn as it is can be problematic - ppl get URLs from traffic analyzer and pirate it.

ask about security concerns upfront.

focus on n/w protocols for bandwidth. edge proxy can have many parts of a movie to have it as close to the users as
possible. its the most complex part.

vpn b/w client and server is used. lot of articles about this. re-record movie as an image.

"""