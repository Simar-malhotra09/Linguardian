import { NextApiRequest, NextApiResponse } from "next";
import { getAllImages } from "@/lib/db";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  try {
    // Log the incoming request and response object for debugging
    console.log("Request Received:", req.method, req.url);
    console.log("Response Object:", res);

    const images = await getAllImages();

    // Log the response status and images before sending the response
    console.log("Response Status:", 500);
    console.log("Response Data:", images);

    res.status(200).json(images);
  } catch (err) {
    console.error("Error fetching images:", err);

    // Log the response status in case of an error
    console.log("Response Status (Error):", 500);
    res.status(500).json({ error: "Failed to fetch images." });
  }
}
