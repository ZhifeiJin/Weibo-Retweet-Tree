I've learned much when writing this program, and I thought my experiences might be helpful to other people who might encounter same issues. 

## New Packages
Packages: selenium, requests
I have no previous experience with selenium and requests. Because the uniqueness of my assignment and Sina Weibo's updates to its websites, there is no currently available package/repository that will do the job. The job, is: 
1) Visit "https://huati.weibo.cn/discovery/super?suda", which contains around 50 lists of Supertopics, each sorted by "influence", which is calculated by Sina itself. I need to get the title, url, and basic information of each Supertopic. 
2) For each Supertopic, I want to get the url and basic information of most recent 200~ posts. 
3) For each post I saved, I want to compute a repost tree.

##Step 1

