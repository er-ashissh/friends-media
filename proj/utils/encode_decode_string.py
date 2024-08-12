from django.conf import settings
import hashlib, json, jwt
from random import randint


# Encode password using MD5, SHA256 and DJANFO AUTH Make Password Hash
def encode_password(password):
    encode_md5 = hashlib.md5(password.encode()).hexdigest()
    encode_sha1 = hashlib.sha256(encode_md5.encode()).hexdigest()
    return encode_sha1


# Encode JSON with base64
def encode_json(param):
    result = jwt.encode(param, settings.JWT_SIGNATURE, algorithm='HS256').decode('utf-8')
    result = str(result)
    result = result.replace('.', 'ixixi')
    return result


# Decode JSON with base64
def decode_json(param):
    result = str(param)
    result = param.replace('ixixi', '.')
    result = bytes(result, 'utf-8') 
    result = jwt.decode(result, settings.JWT_SIGNATURE, algorithms=['HS256'], options={'verify_exp': False})
    return result


# Encrypt RailFence
def encrypt_rail_fence(text, key): 
    rail = [['\n' for i in range(len(text))] 
                  for j in range(key)] 
      
    dir_down = False
    row, col = 0, 0
      
    for i in range(len(text)): 
        if (row == 0) or (row == key - 1): 
            dir_down = not dir_down 
        
        rail[row][col] = text[i] 
        col += 1
          
        if dir_down: 
            row += 1
        else: 
            row -= 1

    result = [] 
    for i in range(key): 
        for j in range(len(text)): 
            if rail[i][j] != '\n': 
                result.append(rail[i][j]) 
    return("" . join(result)) 


# Decrypt RailFence
def decrypt_rail_fence(cipher, key): 
    rail = [['\n' for i in range(len(cipher))]  
                  for j in range(key)] 
      
    dir_down = None
    row, col = 0, 0

    for i in range(len(cipher)): 
        if row == 0: 
            dir_down = True
        if row == key - 1: 
            dir_down = False
        
        rail[row][col] = '*'
        col += 1
          
        if dir_down: 
            row += 1
        else: 
            row -= 1

    index = 0
    for i in range(key): 
        for j in range(len(cipher)): 
            if ((rail[i][j] == '*') and
               (index < len(cipher))): 
                rail[i][j] = cipher[index] 
                index += 1
    
    result = [] 
    row, col = 0, 0
    for i in range(len(cipher)): 
    
        if row == 0: 
            dir_down = True
        if row == key-1: 
            dir_down = False
        
        if (rail[row][col] != '*'): 
            result.append(rail[row][col]) 
            col += 1
        
        if dir_down: 
            row += 1
        else: 
            row -= 1
    return("".join(result)) 
  

''' 
Encrypt eMail based on User ID & Account Type
@request: int: user_id | str: account_type
@response: hash_string
Ex: user_id = 240 | account_type = 'cust' | hash_string: oguareuwltrbhoof
'''
def encrypt_string_email_for_admin(user_id, account_type):
    pure_str = str(user_id) + '_' + str(account_type)
    u_email = ''

    '''
    Convert Number into Alphabet
    - 1 means ja
    - Logic of Number's: 1st months means january, 1st & 3rd index place of january means jn, so on..
    - a means nt
    - Logic of Alphabet's: a + nt means Ant, It's animal or birds name
    '''
    no_to_alpha_dict = {
        '1': ['jn'],
        '2': ['fb'],
        '3': ['mr'],
        '4': ['ar'],
        '5': ['my'],
        '6': ['je'],
        '7': ['jl'],
        '8': ['ag'],
        '9': ['sp'],
        '0': ['ot'],
        'a': ['nt'],
        'b': ['at'],
        'c': ['ow'],
        'd': ['og'],
        'e': ['mu'],
        'f': ['ox'],
        'g': ['oa'],
        'h': ['ye'],
        'i': ['bs'],
        'j': ['au'],
        'k': ['iw'],
        'l': ['io'],
        'm': ['on'],
        'n': ['ew'],
        'o': ['ct'],
        'p': ['ro'],
        'q': ['ua'],
        'r': ['ab'],
        's': ['he'],
        't': ['or'],
        'u': ['gu'],
        'v': ['ut'],
        'w': ['ol'],
        'x': ['ae'],
        'y': ['ak'],
        'z': ['eb'],
        '_': ['ul'],
    }

    '''
    # Check any One Element is Duplicate
    b2_list = [] 
    for k, v in no_to_alpha_dict.items():
        if v[0] in b2_list:
            print('---in--if---', k , v)
        b2_list.append(v[0])
    '''

    # Step I -> Replace the Number & Alphabet to Unique Character
    for i in pure_str:
        u_email += no_to_alpha_dict.get(str(i), ['xx'])[0]

    # Step II -> Encrypt String with RailFence Algo
    u_email =  encrypt_rail_fence(u_email, 3)

    # Step III -> Reverse the String
    u_email = u_email[::-1]

    result = u_email
    return result


def generate_random_numbers(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


def convert_to_slug(name):
    """
    name: str: "Digi Resto Veg "
    return: str: "digi-resto-veg"
    """
    return name.strip().lower().replace(" ", "-")