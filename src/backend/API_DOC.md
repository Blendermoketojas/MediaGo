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
            'theme':'default',
            'genre':'Rock',
            'country':'LT(Ne tikslu dar)'
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
                'theme':'default', 
                'genre':'Rock', 
                'country':'LT(Ne tikslu dar)
            }

4. 