import { NextResponse } from "next/server";


export function middleware(req){    
        
    const url = req.url
    const cookie = req.cookies.get('jwt')
 
    if(url.includes('/cars/add') && (cookie===undefined)){      
            return NextResponse.redirect('http://localhost:3000/account/login')        
    }
    return NextResponse.next()
}
