import cookie from 'cookie'

 
export default async (req, res)=>{
             
    res.status(200).setHeader('Set-Cookie', cookie.serialize(
        'jwt','',
        {
            path:'/',
            httpOnly: true,
            sameSite:'strict',
            maxAge:-1                    
        }
    )    
    
    )
    res.json({"message":"success"})
    res.end()
}