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
  const [imageDimensions, setImageDimensions] = useState<{
    width: number;
    height: number;
  }>({
    width: 0,
    height: 0,
  });

  const getImageSize = () => {
    return {
      width: window.innerWidth,
      height: window.innerHeight,
    };
  };

  useEffect(() => {
    const handleResize = () => {
      const { width, height } = getImageSize();
      setImageDimensions({ width, height });
    };

    handleResize();
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

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
    // Uncomment and use this block when fetching real data
    // async function fetchData() {
    //   try {
    //     const data: Mapping[] = await getMappingsForPage(2);
    //     setMappings(data);
    //   } catch (error) {
    //     console.error("Error fetching mappings:", error);
    //   }
    // }
    // fetchData();
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

        console.log(
          `Mapping ${index}: x=${xPercentage}% y=${yPercentage}% width=${widthPercentage}% height=${heightPercentage}%`
        );

        return (
          <div
            key={index}
            style={{
              position: "absolute",
              top: `${yPercentage}%`,
              left: `${xPercentage}%`,
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
