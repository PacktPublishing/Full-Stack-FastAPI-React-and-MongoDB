import { createContext, useState } from "react";

const AuthContext = createContext({})

export const AuthProvider = ({children}) => {
    const [user, setUser] = useState(null)     
    const [authError, setAuthError] = useState(null)
    const [loading, setLoading] = useState(false)

    return <AuthContext.Provider value={{user, setUser, authError, setAuthError, loading, setLoading}}>
        {children}
    </AuthContext.Provider>
}

export default AuthContext