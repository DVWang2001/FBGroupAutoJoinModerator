from CHECK_MEMBER_MODEL import check_member_facade

ans = [r'加了',
       r'3個共同社團',
       r'4個共同社團'
       ]

url = 'https://www.facebook.com/groups/1121723125941237'

def rule(pages,ans):
    return any(ans[0] in pages.text and ans[i] in pages.text for i in [1, 2])

check_member_facade(ans,url,rule)