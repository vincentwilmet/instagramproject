from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse, JsonResponse
import json 
from urllib.request import urlopen 

class HomePage(View):
    def get(self, request):
        ##header_html = render(request, 'header.html')
        ##footer_html = render(request, 'footer.html')
        ##body_html = render(request, 'body.html')
        #ret = header_html + body_html + footer_html
        ##r = render(request, 'index.html', d)
        ##return "test"
        return render(request, 'main.html')
        ##, 'footer_html', 'body_html')

class HandlePost(View):
    def get(self, request):
        search = request.GET.get("search", "innisfree") 
        result, result['bestLikes'], result['bestPic'] = dict(), -1, None
        result['totalLikes'], result['totalComments'], result['searchInput'] = 0, 0, "Input is: " + search
        url = 'https://www.instagram.com/' + search + '/media/'
        response = urlopen(url)
        data = json.load(response) 
        
        for i in range(1, 11):
            if data['items'][i]['likes']['count'] > result['bestLikes']:
                result['bestLikes'] = data['items'][i]['likes']['count']
                result['bestPic'] = data['items'][i]['link'] 
            result['totalLikes'] += data['items'][i]['likes']['count'] 
            result['totalComments'] += data['items'][i]['comments']['count'] 
        #return HttpResponse(json.dumps(result))
        return render(request, "main.html", result)
         
'''
class HandlePost(View):
    def get(self, request): 
        search = request.GET.get("search", "innisfree") 
        t = request.GET.get("Type", "likes")
        c = request.GET.get("Count", "10")
        url = 'https://www.instagram.com/' + search + '/media/'
        response = urlopen(url)
        data = json.load(response) 
        result = dict()
        if t == 'likes' or t == 'comments':
            for i in range(int(c)):
                pic = data['items'][i]['link'] 
                item = data['items'][i][t]['count']
                result['item'].add(item)
                result['pic'].add(pic)
        else:
            for i in range(int(c)):
                pic = data['items'][i]['link'] 
                item = data['items'][i][t]['count']
                result['item'].add(item)
                result['pic'].add(pic)
        return render(request, result)

'''
