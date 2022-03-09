import requests
import datetime

def calc_age(uid):
    bd_friends = dict()
    token = 'token'
    url = "https://api.vk.com/method/users.get?v=5.81&access_token={token}&user_ids={uid}".format(token=token, uid=uid)
    user_id = requests.get(url).json()["response"][0]["id"]
    url_fr = "https://api.vk.com/method/friends.get?v=5.81&access_token={token}&" \
             "user_id={user_id}&fields=bdate".format(token=token, user_id=str(user_id))
    friends = requests.get(url_fr).json()["response"]["items"]
    for i in range(len(friends)):
        if "bdate" in friends[i].keys():
            if len(friends[i]["bdate"]) >= 8:
                age = datetime.date.today().year - int(friends[i]["bdate"][-4:])
                if age not in bd_friends.keys():
                    bd_friends.setdefault(age, 1)
                else:
                    bd_friends[age] += 1
    bd_list = list(bd_friends.items())
    bd_list.sort(key=lambda x: x[0])
    bd_list.sort(key=lambda x: x[1], reverse=True)
    return bd_list

if __name__ == '__main__':
    res = calc_age('reigning')
    print(res)

