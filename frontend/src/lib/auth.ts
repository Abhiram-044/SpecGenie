export const isTokenValid = (): boolean => {
    if (typeof window === "undefined") return false

    const tokenData = localStorage.getItem("authToken")
    if (!tokenData) return false

    try {
        const { expiry } = JSON.parse(tokenData)

        if (Date.now() > expiry) {
            localStorage.removeItem("authToken")
            return false
        }

        return true
    } catch {
        return false
    }
}