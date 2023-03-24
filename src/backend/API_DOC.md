Čia rašomas visas API veikimas su duomenų siuntimo pavyzdžiais bei galimais response

SVARBU:
    DEFAULT API response gali būti:
        1. Nusiunčiant blogai sukonfigūruotus JSON 'keys'
            {
                'success':False,
                'message':'JSON keys not supported!'
            }
        2. Nusiunčiant blogą duomenų tipą
            {
                'success':False,
                'message':'Content type not supported'
            }
        

API:
== - tai http adresas į API, arba mano IP adresas su portu arba localhost
1. ==/register ; priimamas metodas POST
    Priimamo JSON objekto pvz.:
        {
            'nickname':'tadelis',
            'email':'tadelistadelis@gmail.com',
            'password':'tadelis123'
        }

    Galimas grįžtamas ryšys:
        1. Duomenų bazėje įvyko vartotojų vardų atitikimas
            {
                'success':False,
                'message':'nickname'
            }
        2. Duomenų bazėje įvyko elektroninių paštų atitikimas
            {
                'success':False,
                'message':'email'
            }
        3. Nebuvo jokių kliūčių ir naujas vartotojas buvo užregistruotas
            {
                'success':True,
                'id':/sukurtas vartotojo ID/,
                'nickname':'tadelis'
            }

2. ==/login ; priimamas metodas POST
    priimamo JSON objekto pvz.:
        {
            'email':'tadelistadelis@gmail.com',
            'password':'tadelis123'
        }

    Galimas grįžtamas ryšys:
        1. Nebuvo rasta elektroninio pašto atitikčių duomenų bazėję
            {
                'success':False,
                'message':email
            }
        2. Neatitiko slaptažodis su išsaugotu duomenų bazėję
            {
                'success':False,
                'message':'password'
            }
        3. Viskam atitikus siunčiami šie duomenys:
            {
                'success':True,
                'id':/vartotojo id/,
                'nickname':'tadelis'
            }

3. ==/server_add ; priimamas metodas POST
    priimamo JSON objekto pvz.:
        {
            'name':'CoolHole',
            'owner':/vartotojo id/,
            'description':'Kieta skyle',
            'theme':1,
            'genre':1,
            'country':5
        }

    Galimas grįžtamas ryšys:
        1. Buvo surastas išsaugotas kambarys su tokiu pačiu pavadinimu
            {
                'success':False,
                'message':'name'
            }
        2. Jokių problemų neatsirado ir išsaugojami duomenys apie kambarį
            {
                'success':True, 
                'id':/sukurtas kambario id/, 
                'name':'CoolHole', 
                'owner':/vartotojo id/,
                'description':'Kieta skyle', 
                'theme':1, 
                'genre':1, 
                'country':5
            }

4. ...

#. ==/get_server_info?id=/id/ : priimamas metodas GET
    pvz.: ==/get_server_info?id=1
    
    1. Gaunamas JSON objektas jeigu yra rastas kambarys su šiuo ID:
            {
                'success':True, 
                'id':/sukurtas kambario id/, 
                'name':'CoolHole', 
                'owner':/vartotojo id/,
                'description':'Kieta skyle', 
                'theme':1, 
                'genre':1, 
                'country':5
            }
    
    2. Gaunamas JSON objektas jeigu nėra rastas kambarys su šiuo ID:
            {
                'success':False, 
                'message':'id'
            }

#. ==/get_dropdown_search?type=/tipas/ ; priimamas metodas GET
    1. tipas - genre pvz.: /get_dropdown_search?type=genre | grąžina visus žanrus kurie yra panaudoti egzistuojančiuose kambariuose.
        Gauto JSON objekto pvz.:
            {"data":{
                "0":{
                    "id":1,
                    "name":"Rock"
                    },
                "1":{
                    "id":2,
                    "name":"Pop"
                    },
                "2":{
                    "id":3,
                    "name":"Hip Hop"
                    },
                    ...
                },
            "success":true
            }
    2. tipas - country pvz.: /get_dropdown_search?type=country | grąžina visas šalis kurios yra panaudotos egzistuojančiuose kambariuose.
        Gauto JSON objekto pvz.:
            {
            "data":{
                "0":{
                    "id":1,
                    "name":"Afghanistan"
                    },
                "1":{
                    "id":2,
                    "name":"Albania"
                    },
                "2":{
                    "id":3,
                    "name":"Algeria"
                    },
                    ...
                },
            "success":true
            }
    [KOMENTARAS] Jeigu grąžinto JSON objekto "data" masyvas yra tuščias, reiškia, kad nebuvo rasti elementai kurie būtų panaudoti egzistuojančiuose kambariuose (nėra sukurtų kambarių DB)

    3. Nurodant blogai tipą grąžinamas toks JSON objektas:
        {
            'success':False, 
            'message':'Argument not supported'
        }

#. ==/get_dropdown_create?type=/tipas/ ; priimamas metodas GET
    1. tipas - genre pvz.: /get_dropdown_create?type=genre | grąžina visus žanrus kurie yra duomenų bazėje.
        Gauto JSON objekto pvz.:
            {"data":{
                "0":{
                    "id":1,
                    "name":"Rock"
                    },
                "1":{
                    "id":2,
                    "name":"Pop"
                    },
                "2":{
                    "id":3,
                    "name":"Hip Hop"
                    },
                    ...
                },
            "success":true
            }
    2. tipas - country pvz.: /get_dropdown_create?type=country | grąžina visas šalis kurios yra duomenų bazėje.
        Gauto JSON objekto pvz.:
            {
            "data":{
                "0":{
                    "id":1,
                    "name":"Afghanistan"
                    },
                "1":{
                    "id":2,
                    "name":"Albania"
                    },
                "2":{
                    "id":3,
                    "name":"Algeria"
                    },
                    ...
                },
            "success":true
            }
    [KOMENTARAS] Jeigu grąžinto JSON objekto "data" masyvas yra tuščias, nėra supushinti duomenys į duomenų bazę.

    3. Nurodant blogai tipą grąžinamas toks JSON objektas:
        {
            'success':False, 
            'message':'Argument not supported'
        }