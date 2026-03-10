import { apiConnector } from "@/lib/apiConnector";
import { useMagicLinkStore } from "@/store/useMagicLinkStore";
import { toast } from "sonner";
import { authEndpoints } from "@/services/apis";
import { CreateAccountResponse, LoginResponse, SignUpResponse } from "@/types/auth";

const {
  REGISTER_INITIATE_API,
  REGISTER_COMPLETE_API,
  LOGIN_API,
  LOGOUT_API
} = authEndpoints;

export const registerInitiate = async (email: string) => {
  try {
    const response = await apiConnector<SignUpResponse>(
      "POST",
      REGISTER_INITIATE_API,
      { email }
    );
    if (response.data.success) {
      const token = response.data.magic_token;
      useMagicLinkStore.getState().setMagicLink(token);
      return response.data;
    } else {
      throw new Error(response.data.message || "Failed to send link");
    }
  } catch (error: any) {
    const errorMessage = error?.response?.data?.message || "Something went wrong";
    throw new Error(errorMessage);
  }
};

type Navigate = (path: string) => void

export async function registerComplete(
  username: string,
  password: string,
  confirmPassword: string,
  token: string
): Promise<any> {
  const response = await apiConnector<CreateAccountResponse>(
    "POST",
    REGISTER_COMPLETE_API(token),
    {
      "username": username,
      "password": password,
      "confirm_password": confirmPassword,
    }
  )

  if (!response.data.success) {
    throw new Error(response.data.message || "Registration failed")
  }

  return response.data;
}

export async function login(
  eUser: string,
  password: string
): Promise<LoginResponse> {
  const formData = new URLSearchParams();
  formData.append("username", eUser);
  formData.append("password", password);

  try {
    const response = await apiConnector<LoginResponse>(
      "POST",
      LOGIN_API,
      formData,
      {
        "Content-Type": "application/x-www-form-urlencoded",
      }
    );

    if (response.data.success && response.data.access_token) {
      const token = response.data.access_token;
      const expiry = Date.now() + 7 * 24 * 60 * 60 * 1000;

      localStorage.setItem(
        "authToken",
        JSON.stringify({ token, expiry })
      );

      return response.data;
    } else {
      throw new Error("Invalid Credentials");
    }
  } catch (error: any) {
    const errorMessage = error?.response?.data?.message || "Login failed";
    throw new Error(errorMessage);
  }
}

export async function logout(navigate: Navigate): Promise<void> {
  console.log("Logging out")

  try {
    const storedToken = localStorage.getItem("authToken")

    let token = ""

    if (storedToken) {
      const parsed = JSON.parse(storedToken)
      token = parsed.token
    }

    await apiConnector(
      "POST",
      LOGOUT_API,
      null,
      {
        Authorization: `Bearer ${token}`,
      }
    )
    localStorage.removeItem("authToken")

    toast.success("Logged out successfully", {
      duration: 3000,
      style: {
        border: "1px solid rgba(47, 200, 122, 0.5)",
        backgroundColor: "rgba(47, 200, 122, 0.1)",
        color: "#2fc87a"
      }
    })

    setTimeout(() => {
      navigate("/login")
    }, 1000)

  } catch (error: any) {
    console.log("Error logging out", error)

    const errorMessage =
      error?.response?.data?.message || "Failed to logout"

    toast.error(error, {
      style: {
        border: "1px solid rgba(251, 44, 54, 0.5)",
        backgroundColor: "rgba(251, 44, 54, 0.1)",
        color: "#fb2c36"
      }
    })
  }
}