# PMS plugin framework
import datetime,re


##################################################################################################AS
VIDEO_PREFIX     = "/video/adultswim"
NAME          = L('Title')

AS_URL                     = "http://www.adultswim.com"
AS_VIDURL                     = "http://video.adultswim.com"
AS_FULL_EPISODES_SHOW_LIST = "http://video.adultswim.com/episodes/index.html"

AS_FEED                    = "http://www.adultswim.com/"
DEBUG                       = False
ASart                      ="art-default.jpg"
ASthumb                    ="icon-default.jpg"

####################################################################################################

def Start():
  Plugin.AddPrefixHandler(VIDEO_PREFIX, VideoMainMenu, '[adult swim]',ASthumb,ASart)
  Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
  Plugin.AddViewGroup("List", viewMode="List", mediaType="items")
  
  MediaContainer.art        =R(ASart)
  MediaContainer.title1     = NAME
  DirectoryItem.thumb       =R(ASthumb)

####################################################################################################
#def VideoMainMenu():
#    dir = MediaContainer(mediaType='video') 
#    dir.Append(Function(DirectoryItem(all_shows, "All Shows"), pageUrl = AS_FULL_EPISODES_SHOW_LIST))
#    return dir
    
####################################################################################################
def VideoMainMenu():
    pageUrl=AS_FULL_EPISODES_SHOW_LIST
    dir = MediaContainer(viewGroup="List")
    content1 = XML.ElementFromURL(pageUrl, isHTML="True")
    showMap = dict()
    shownum=0
    for item in content1.xpath('//div[@id="adultswim-episodes"]'):
        Log(item)
        Log(item.findall('./div/dl/dd/a'))
        things = item.findall('./div/dl/dd/a')
        
        for thingies in things:
          shownum =shownum+1
          showID=shownum
          Log(thingies)
          title=thingies.text
          titleUrl=thingies.get('href')
          titleUrl=AS_VIDURL + titleUrl
          thumb=ASthumb
          Log(titleUrl)
          Log(title)
      #  Log(thumb)
          showList = showMap.get(title)
          if showList == None:
		      showList = []
		      showMap[title] = showList
		  # Tuple order here matters
          showList.append((showID,titleUrl, thumb, title))
          Log(showList)
    shows=showMap.keys()
    Log(shows)
    shows.sort()
    Log(shows)
    shownum=0
    #for shownames in shows:
    #  shownum=shownum+1
    #  showList.append((shownum,shownames.titleUrl,shownames.thumb, shownames.title))
    for showkey in shows:
      Log(showkey)
      for show in showMap[showkey]:
        Log(show)
        title=show[3]
        url=show[1]
        thumb=show[2]
        Log("Show: " + title + " | link: " + url)
        dir.Append(Function(DirectoryItem(showxml, title=title), pageUrl = url))
      
    
    return dir 
####################################################################################################


####################################################################################################
def showxml(sender, pageUrl):
  dir = MediaContainer(title2=sender.itemTitle, viewGroup="InfoList", noCache=True)
  content = XML.ElementFromURL(pageUrl, isHTML="True")
  showID=content.xpath('//head/meta[@name="collectionId"]')[0].get('content')
  Log(showID)
  link="http://www.adultswim.com/adultswimdynamic/asfix-svc/episodeSearch/getAllEpisodes?limit=15&offset=0&sortByDate=DESC&categoryName=Comedy&filterByEpisodeType=PRE,EPI,CLI&filterByCollectionId=" + showID + "&networkName=AS"
  shows=XML.ElementFromURL(link).xpath('//episodes/episode')
  Log(shows)
  for show in shows:
    Log(show)
    #episodeID  
    epID=show.get('episodeNumber')

    #title
    title=show.get('title')

    #thumb
    thumb=show.get('thumbnailUrl')
    #summary
    summary=show.xpath('./description')[0].text
    #link
    clip=show.xpath('./episodeLink')[0].get('episodeUrl') 
    
    if(int(epID)< 100):
      title="Episode: " + title
    if(int(epID)> 100):
      title="Clip: " + title

    Log("epID: " + epID + " | title: " + title + " | thumb: " + thumb + " | Description: " + summary)
    dir.Append(WebVideoItem(clip, title=title, thumb=thumb, summary=summary))

  return dir
