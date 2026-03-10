const BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

export const authEndpoints = {
    REGISTER_INITIATE_API: `${BASE_URL}/auth/register/initiate`,
    REGISTER_COMPLETE_API: (token: string) => `${BASE_URL}/auth/register/complete/${token}`,
    LOGIN_API: `${BASE_URL}/auth/login`,
    LOGOUT_API: `${BASE_URL}/auth/logout`,
}