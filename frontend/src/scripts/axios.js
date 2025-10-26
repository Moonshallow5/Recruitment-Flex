import axios from "axios";
import Store from "@/states/store.js";
import { useToast } from "vue-toast-notification";
import "vue-toast-notification/dist/theme-sugar.css";

const $toast = useToast();

const API_URL = import.meta.env.VITE_API_URL;
const APP_DEBUG = import.meta.env.VITE_APP_DEBUG;

export default async (
  url,
  payload = {},
  method = "POST",
  params = {},
  custom_err_response = null,
) => {
  const token = Store.state.token;
  const headers = {
    "Content-Type": "application/json",
    Accept: "application/json",
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const full_url = `${API_URL}/${encodeURI(url)}`;
  try {
    if (APP_DEBUG) {
      console.log("Request URL:", full_url);
      console.log(
        `Request Payload: ${JSON.stringify(
          payload,
        )} and params: ${JSON.stringify(params)}`,
      );
    }

    if (method === "GET") {
      params = payload;
    }

    const response = await axios({
      headers,
      method,
      url: full_url,
      params,
      data: payload,
      timeout: 30000,
    });

    if (APP_DEBUG) {
      console.log("Response:", response.data);
    }

    if (response.status >= 400) {
      if (!custom_err_response) {
        $toast.error(response.data.message || "An error occurred", {
          duration: 3000,
          position: "top-right",
        });
      } else {
        custom_err_response(response.data);
      }

      if (response.status === 401) {
        const original_path = `/`;
        Store.commit("resetState");
        if (window.location.pathname !== original_path) {
          window.location.href = original_path;
        }
      }
    }

    return response.data;
  } catch (error) {
    if (APP_DEBUG) {
      console.error("Error:", error.response);
      console.log(error.request);
    }

    const errorMessage = error.response?.data?.detail || error.response?.data?.message || error.message;
    $toast.error(errorMessage, {
      duration: 3000,
      position: "top-right",
    });

    Store.commit("clearLoading");

    throw error;
  }
};

