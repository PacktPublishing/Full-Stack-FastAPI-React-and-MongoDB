import cookie from 'cookie'
 
export default async (req, res)=>{
    if (req.method==='POST'){

        const {email, password} = req.body

        const result = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/users/login`, {
            method:'POST',
            headers:{'Content-Type':'application/json'},
            body:JSON.stringify({email, password})
        })

        const data = await result.json() 
        if (result.ok){
            const jwt = data.token            
            res.status(200).setHeader('Set-Cookie', cookie.serialize(
                'jwt',jwt,
                {
                    path:'/',
                    httpOnly: true,
                    sameSite:'strict',
                    maxAge:1800
                    
                }
            )).json({
                'username':data['user']['username'],
                'email':data['user']['email'],
                'role':data['user']['role'],
                'jwt':jwt
            })
        } else {
           
            data['error'] = data['detail']
            res.status(401)
            res.json(data)
            return
        }

        
    } else {
        res.setHeader('Allow',['POST'])
        res.status(405).json({message:`Method ${req.method} not allowed`})
        return
    }
}