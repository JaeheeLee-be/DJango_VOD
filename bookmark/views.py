from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from bookmark.models import Bookmark
# from django.http import Http404

def bookmark_list(request):
    bookmarks = Bookmark.objects.filter(id__gte=50)
    # SELECT * FROM bookmark

    context = {
        'bookmarks': bookmarks
    }
    # return HttpResponse('<h1>북마크 리스트 페이지입니다.</h1>')
    return render(request, 'bookmark_list.html', context)

def bookmark_detail(request, pk):
    # try:
    #     bookmark = Bookmark.objects.get(pk=pk)
    # except:
    #     raise Http404
    bookmark = get_object_or_404(Bookmark, pk=pk)

    context = {'bookmark': bookmark}
    return render(request, 'bookmark_detail.html', context)

# bookmark = Bookmark.objects.all()
# SELECT * FROM bookmark

# Bookmark: [Bookmark] = Bookmark.objects.get(pk=pk)
# SELECT * FROM bookmark WHERE id=id LIMIT 1

# Bookmark: [Bookmark]= Bookmark.objects.filter(name='네이버')
# SELECT * FROM bookmark WHERE name='네이버'
# like search
# Bookmark: [Bookmark]= Bookmark.objects.filter(name__icontains='네이버')
# SELECT * FROM bookmark WHERE name LIKE '%네이버%'

# now = datetime.now(), gt(오늘보다 나중에 만들어진 것)
# Bookmark: [Bookmark]= Bookmark.objects.filter(created_at_gte=now), gte(오늘 포함해서 오늘 이후에 만들어진 것)
# SELECT * FROM bookmark WHERE created_at > now
# Bookmark: [Bookmark]= Bookmark.objects.filter(created_at_lte=now), lte(오늘 포함해서 오늘 이전에 만들어진 것)
# SELECT * FROM bookmark WHERE created_at <= now
# Bookmark: [Bookmark]= Bookmark.objects.filter(created_at_lt=now), lt(오늘보다 이전에 만들어진 것)
# SELECT * FROM bookmark WHERE created_at < now

# Bookmark.objects.bulk_create DB요청 횟수를 줄이기 때문에 한 번에 많은 양의 create와 update를 할 때 사용, for문은 돌 때마다 DB 요청