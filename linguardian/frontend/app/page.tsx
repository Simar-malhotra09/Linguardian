"use client";

import { useEffect, useState } from "react";
import { CldImage } from "next-cloudinary";
import { getMappingsForPage } from "@/lib/db";

type Mapping = {
  boundingBox: { x: number; y: number; width: number; height: number };
  originalWord: string;
};

export default function Page() {
  const [mappings, setMappings] = useState<Mapping[]>([]);

  const [distanceFromLeft, setDistanceFromLeft] = useState(0);

  useEffect(() => {
    const dummyMappings: Mapping[] = [
      // For now, fill with dummy data for testing
      {
        boundingBox: { x: 227, y: 170, width: 94, height: 24 },
        originalWord: "School",
      },
      {
        boundingBox: { x: 382, y: 259, width: 62, height: 17 },
        originalWord: "Mearii",
      },
      {
        boundingBox: { x: 454, y: 264, width: 31, height: 12 },
        originalWord: "san",
      },
      {
        boundingBox: { x: 228, y: 382, width: 77, height: 29 },
        originalWord: "Major",
      },
    ];
    setMappings(dummyMappings);
  }, []);
  useEffect(() => {
    const image = document.getElementById("myImage") as HTMLImageElement | null;

    if (image) {
      const rect = image.getBoundingClientRect();
      const distanceFromLeft = rect.left;
      console.log(
        `Distance from the left edge of the browser to the image: ${distanceFromLeft}px`
      );
      setDistanceFromLeft(distanceFromLeft);
    }
  }, []);

  return (
    <div
      style={{
        position: "relative",
        overflow: "hidden",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      {/* Background Image */}
      <CldImage
        id="myImage"
        src="local_image" // Replace with your Cloudinary image public ID or path
        alt="Etext-style image"
        width={1417}
        height={2028}
        quality="auto"
        format="auto"
        style={{ objectFit: "contain" }}
      />

      {/* Overlay Divs */}
      {mappings.map((mapping, index) => {
        // Dynamically scale bounding boxes based on image dimensions
        const xPercentage = (mapping.boundingBox.x / 1417) * 100;
        const yPercentage = (mapping.boundingBox.y / 2028) * 100;
        const widthPercentage = (mapping.boundingBox.width / 1417) * 100;
        const heightPercentage = (mapping.boundingBox.height / 2028) * 100;

        const adjustedXPercentage = xPercentage + 10;

        return (
          <div
            key={index}
            style={{
              position: "absolute",
              top: `${yPercentage}%`,
              left: `${adjustedXPercentage}%`,
              width: `${widthPercentage}%`,
              height: `${heightPercentage}%`,
              backgroundColor: "black", // Set the background color inside the bbox
              color: "white", // Text color for the word
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              pointerEvents: "none", // Ensures the overlay does not block image interactions
              border: "2px solid red", // Optional: for a border around the bbox
            }}
          >
            {mapping.originalWord}{" "}
            {/* Display the original word inside the bbox */}
          </div>
        );
      })}
    </div>
  );
}
