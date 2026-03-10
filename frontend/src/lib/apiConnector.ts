import axios, { AxiosRequestConfig, AxiosResponse, Method } from "axios";

export const axiosInstance = axios.create({
    baseURL: process.env.NEXT_PUBLIC_API_BASE_URL,
    withCredentials: true
})

export async function apiConnector<T>(
    method: Method,
    url: string,
    bodyData?: unknown,
    headers?: Record<string, string>, 
    params?: Record<string, string | number | boolean>, 
): Promise<AxiosResponse<T>> {
    const config: AxiosRequestConfig = {
        method,
        url,
        data: bodyData,
        headers,
        params,
    };

    return axiosInstance(config);
}