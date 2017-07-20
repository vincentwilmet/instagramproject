from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse, JsonResponse
from urllib.request import urlopen 
import json, gspread, datetime 
from oauth2client.service_account import ServiceAccountCredentials

#share with instagramproject-500@instaproject-171520.iam.gserviceaccount.com

def uploadToGoogleSheets(search, bestLikes, bestPic, totalLikes, totalComments, followers):
    #credentials
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    #opening the spreadsheet: client.open(file name), then sheet.worksheet(worksheet name)
    today = datetime.date.today()
    sheet = client.open('innisfree Community Management Data') 
    worksheet = sheet.worksheet('Instagram')
    columnA = worksheet.col_values(1) #column 1
    for i in range(1, len(columnA)):  
        if columnA[i] == "":  
            row, index = [str(today), search, bestLikes, bestPic, totalLikes, totalComments, followers], i + 1
            #input: [07-07-2017, innisfree, 100, sourcepic, 1000, 10, 10000]
            worksheet.insert_row(row, index)
            break #stops it from putting an input in every cell after
        elif columnA[i] == str(today):  
            row, index = [str(today), search, bestLikes, bestPic, totalLikes, totalComments, followers], i + 1
            #input: [07-07-2017, innisfree, 100, sourcepic, 1000, 10, 10000]
            worksheet.insert_row(row, index)
            print("deleting now")
            worksheet.delete_row(index + 1) #deletes the row that was already input today
            break 


class HomePage(View):
    #called from urls.py to load main.html as the default landing page
    def get(self, request): 
        return render(request, 'main.html') 

class HandlePost(View):
    def get(self, request):
        #after clicking submit on localhost, this function is launched
        search = request.GET.get("search", "innisfree") 
        result, result['bestLikes'], result['bestPic'], result['followers'] = dict(), -1, None, -1
        result['totalLikes'], result['totalComments'], result['searchInput'] = 0, 0, search 
        #load the user's json data
        url = 'https://www.instagram.com/' + search + '/?__a=1' 
        response = urlopen(url) 
        data = json.load(response)   

        #last 11 posts except the most recent
        for i in range(1, 11):
            likes = data['user']['media']['nodes'][i]['likes']['count'] 
            comments = data['user']['media']['nodes'][i]['comments']['count'] 
            #testing to see what is the most liked post
            if likes + comments > result['bestLikes']:
                result['bestLikes'] = likes +  comments
                result['bestPic'] = data['user']['media']['nodes'][i]['display_src'] 
            #making a total
            result['totalLikes'] += likes 
            result['totalComments'] += comments

        result['followers'] = data['user']['followed_by']['count']
        result['searchInput'] = data['user']['full_name']
        print("hi") #printing to see if there were no errors up until google sheets steps
        uploadToGoogleSheets(result['searchInput'], result['bestLikes'], result['bestPic'], 
                                result['totalLikes'], result['totalComments'], result['followers']) 
        print("hi again") #printing to see if we made it past the google sheets steps
        return HttpResponse(json.dumps(result)) #for json response
        #return render(request, "main.html", result) #for webpage reset response
 