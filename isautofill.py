import requests


class Isautofill:

    def __init__(self,dev_key,region='br1'):
        self.region = region
        self.dev_key = dev_key
        self.common_path = f"https://{region}.api.riotgames.com"

    def _get_summoner(self,summoner_name):
        r = requests.get(f"{self.common_path}/lol/summoner/v3/summoners/by-name/{summoner_name}?api_key={self.dev_key}")
        return r.json()

    def _get_rank(self, summonerId):
        r = requests.get(f"{self.common_path}/lol/league/v3/positions/by-summoner/{summonerId}?api_key={self.dev_key}")
        return r.json()

    def _get_winrate(self, ranked_json):
        wins = ranked_json[0]['wins']
        losses = ranked_json[0]['losses']
        return int((wins/(wins+losses))*100)

    def _get_nmatches(self, ranked_json,accountId):
        wins = ranked_json[0]['wins']
        losses = ranked_json[0]['losses']
        nranked = wins+losses
        if nranked <= 100:
            nranked = nranked
        else:
            nranked = 100
        r = requests.get(f'{self.common_path}/lol/match/v3/matchlists/by-account/{accountId}?api_key={self.dev_key}',params={'beginIndex':0,'endIndex':nranked,'queue':[420]})
        return r.json()

    def _get_mainrole(self, matches_json):
        role_dic = {"MID":0,"DUO_SUPPORT":0,"DUO_CARRY":0,"DUO":0,"JUNGLE":0,"TOP":0,"NONE":0,"SOLO":0}
        for li in matches_json['matches']:
            if li['lane'] == "BOTTOM":
                role_dic[li['role']] += 1
            else:
                role_dic[li['lane']] += 1
        maxl = []
        for k,v in role_dic.items():
            maxl.append(v)
        max1 = max(maxl)
        maxl.pop(maxl.index(max1))
        max2 = max(maxl)
        maxkeyd = {}
        for k,v in role_dic.items():
            if v == max1:
                maxkeyd[k] = v
            elif v == max2:
                maxkeyd[k] = v
        return maxkeyd

    def _get_matchplayers(self,summonerId):
        r = requests.get(f'{self.common_path}/lol/spectator/v3/active-games/by-summoner/{summonerId}?api_key={self.dev_key}')
        data = r.json()
        sum_li = []
        for li in data['participants']:
            sum_li.append(li['summonerName'])
        return sum_li

    def is_all_autofill(self,sum_name):
        subject = self._get_summoner(sum_name)
        print(subject)
        sum_li = self._get_matchplayers(subject["id"])
        for li in sum_li:
            individual = self._get_summoner(li)
            rank_data = self._get_rank(individual['id'])
            nmatches = self._get_nmatches(rank_data,individual['accountId'])
            mainrole = self._get_mainrole(nmatches)
            winrate = self._get_winrate(rank_data)
            print(f'{li} || Main roles (role/games played): {mainrole} || Winrate: {winrate}')

# example
if __name__=='__main__':
    riot = Isautofill("dev key here")
    riot.is_all_autofill("summoner's name here")
