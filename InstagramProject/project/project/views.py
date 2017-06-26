from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse, JsonResponse
from urllib.request import urlopen 
import json, gspread, datetime
from oauth2client.service_account import ServiceAccountCredentials

def uploadToGoogleSheets(search, bestLikes, bestPic, totalLikes, totalComments, followers):
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    date = datetime.date.today()
    sheet = client.open('innisfree') 
    worksheet = sheet.worksheet('Instagram')
    l = worksheet.col_values(1)
    for i in range(1, len(l)): 
        if l[i] == date:
            row, index = [str(date), search, bestLikes, bestPic, totalLikes, totalComments, followers], i
            worksheet.insert_row(row, index)
            break
        elif l[i] == "": 
            row, index = [str(date), search, bestLikes, bestPic, totalLikes, totalComments, followers], i
            worksheet.insert_row(row, index)
            break

class HomePage(View):
    def get(self, request): 
        return render(request, 'main.html') 

class HandlePost(View):
    def get(self, request):
        search = request.GET.get("search", "innisfree") 
        result, result['bestLikes'], result['bestPic'], result['followers'] = dict(), -1, None, -1
        result['totalLikes'], result['totalComments'], result['searchInput'] = 0, 0, search
        url = 'https://www.instagram.com/' + search + '/?__a=1' 
        response = urlopen(url) 
        data = json.load(response)  
        
        for i in range(1, 11):
            if data['user']['media']['nodes'][i]['likes']['count'] > result['bestLikes']:
                result['bestLikes'] = data['user']['media']['nodes'][i]['likes']['count']
                result['bestPic'] = data['user']['media']['nodes'][i]['display_src'] 
            
            result['totalLikes'] += data['user']['media']['nodes'][i]['likes']['count'] 
            result['totalComments'] +=data['user']['media']['nodes'][i]['comments']['count']
        result['followers'] = data['user']['followed_by']['count']
        result['searchInput'] = data['user']['full_name'] 
        uploadToGoogleSheets(result['searchInput'], result['bestLikes'], result['bestPic'], 
                                result['totalLikes'], result['totalComments'], result['followers']) 

        return HttpResponse(json.dumps(result)) #for json response
        #return render(request, "main.html", result) #for webpage
    
