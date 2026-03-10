export interface SignUpResponse {
    success: boolean;
    message: string;
    magic_token: string;
}

export interface CreateAccountResponse {
    success: boolean;
    message: string;
}

export interface LoginResponse {
    success: boolean;
    access_token: string;
}