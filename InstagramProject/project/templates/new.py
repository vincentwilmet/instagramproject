from urllib.request import urlopen 
import json, gspread, datetime 
from oauth2client.service_account import ServiceAccountCredentials

#share with instagramproject-500@instaproject-171520.iam.gserviceaccount.com

def uploadToGoogleSheets(search, bestLikes, bestPic, totalLikes, totalComments, followers, caption, PostPerDay):
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    today = datetime.date.today()
    sheet = client.open('Tool') 
    worksheet = sheet.worksheet('Instagram')
    columnA = worksheet.col_values(1)
    for i in range(1, len(columnA)):  
        if columnA[i] == str(today): 
            row, index = [str(today), search, bestLikes, bestPic, totalLikes, totalComments, followers, caption, str(PostPerDay)], i+1
            worksheet.insert_row(row, index)
            break
        elif columnA[i] == "":  
            row, index = [str(today), search, bestLikes, bestPic, totalLikes, totalComments, followers, caption, str(PostPerDay)], i
            worksheet.insert_row(row, index)
            break

def Main(): 
    print("search for")
    search = input("") 
    result, result['bestLikes'], result['bestPic'], result['followers'] = dict(), -1, None, -1
    result['totalLikes'], result['totalComments'], result['searchInput'] = 0, 0, search 

    url = 'https://www.instagram.com/' + search + '/?__a=1' 
    response = urlopen(url) 
    data = json.load(response)  
    
    for i in range(1, 11):
        if data['user']['media']['nodes'][i]['likes']['count'] > result['bestLikes']:
            result['bestLikes'] = data['user']['media']['nodes'][i]['likes']['count']
            result['bestPic'] = data['user']['media']['nodes'][i]['display_src'] 
            result['caption'] = data['user']['media']['nodes'][i]['caption']
        
        result['totalLikes'] += data['user']['media']['nodes'][i]['likes']['count'] 
        result['totalComments'] += data['user']['media']['nodes'][i]['comments']['count']
    
    result['followers'] = data['user']['followed_by']['count']
    result['searchInput'] = data['user']['full_name']
    oldestPostDate = data['user']['media']['nodes'][11]['date']
    newestPostDate = data['user']['media']['nodes'][1]['date'] 
    result['#PostPerDay'] =  10 / ( ( newestPostDate - oldestPostDate ) / ( 60 * 60 * 24 ) ) 

    uploadToGoogleSheets(result['searchInput'], result['bestLikes'], result['bestPic'], 
                            result['totalLikes'], result['totalComments'], result['followers'], 
                            result['caption'], result['#PostPerDay']) 
    print("hi again") 
    return result
 
Main()