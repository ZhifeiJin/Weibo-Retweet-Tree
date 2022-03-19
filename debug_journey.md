I've learned much when writing this program, and I thought my experiences might be helpful to other people who might encounter same issues.

## Sina Weibo API

I tried the Sina Weibo API at first, and it turned out to be not so helpful. I wanted to get specific information about too many posts and from Supertopics, which is not a feature in the API. Therefore, I had to write a program that is tailored for my purposes.

## New Packages

Packages: selenium, requests
I have no previous experience with selenium and requests. Because the uniqueness of my assignment and Sina Weibo's updates to its websites, there is no currently available package/repository that will do the job. The job, is:

1. Visit "https://huati.weibo.cn/discovery/super?suda", which contains around 50 lists of Supertopics, each sorted by "influence", which is calculated by Sina. I need to get the title, url, and basic information of each Supertopic.
2. For each Supertopic, I want to get the url and basic information of most recent 200~ posts.
3. For each post I saved, I want to compute a repost tree.

## Step 1

The original plan was to get first 100 Supertopics of each list, so it would give me 5000 Supertopics to crawl. The number #21-100 Supertopics requires scrolling only _a section of_ the webpage. Scrolling the webpage was easy, but locating the (middle) section to scroll was hard. I tried clicking somewhere in the middle section and then button down (do key_down for around 1000 times did the trick), but
