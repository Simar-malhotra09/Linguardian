"use client";

import { useEffect, useState } from "react";
import { CldImage } from "next-cloudinary";
import { getMappingsForPage } from "@/lib/db";

type Mapping = {
  boundingBox: { x1: number; x2: number; y1: number; y2: number };
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

  useEffect(() => {
    const dummyMappings: Mapping[] = [
      {
        boundingBox: {
          x1: 0.1213832039520113,
          x2: 0.1743119266055046,
          y1: 0.08444444444444445,
          y2: 0.09580246913580247,
        },
        originalWord: "Class",
      },
      {
        boundingBox: {
          x1: 0.31898376852505295,
          x2: 0.36203246294989416,
          y1: 0.0874074074074074,
          y2: 0.09876543209876543,
        },
        originalWord: "your",
      },
      {
        boundingBox: {
          x1: 0.3697953422724065,
          x2: 0.4798870853916726,
          y1: 0.08444444444444445,
          y2: 0.0962962962962963,
        },
        originalWord: "classmates",
      },
      {
        boundingBox: {
          x1: 0.4890613973182781,
          x2: 0.5356386732533521,
          y1: 0.08493827160493828,
          y2: 0.0962962962962963,
        },
        originalWord: "what",
      },
      {
        boundingBox: {
          x1: 0.544107268877911,
          x2: 0.5871559633027523,
          y1: 0.08493827160493828,
          y2: 0.0962962962962963,
        },
        originalWord: "their",
      },
      {
        boundingBox: {
          x1: 0.5963302752293578,
          x2: 0.6612561750176429,
          y1: 0.08493827160493828,
          y2: 0.09925925925925926,
        },
        originalWord: "majors",
      },
      {
        boundingBox: {
          x1: 0.7141848976711362,
          x2: 0.7494707127734651,
          y1: 0.08493827160493828,
          y2: 0.09679012345679013,
        },
        originalWord: "and",
      },
      {
        boundingBox: {
          x1: 0.7586450247000706,
          x2: 0.7939308398023994,
          y1: 0.0854320987654321,
          y2: 0.09679012345679013,
        },
        originalWord: "find",
      },
      {
        boundingBox: {
          x1: 0.8038108680310515,
          x2: 0.8934368383909669,
          y1: 0.08839506172839506,
          y2: 0.09679012345679013,
        },
        originalWord: "someone",
      },
      {
        boundingBox: {
          x1: 0.12067748764996472,
          x2: 0.16090331686661963,
          y1: 0.10518518518518519,
          y2: 0.11654320987654321,
        },
        originalWord: "who",
      },
      {
        boundingBox: {
          x1: 0.16937191249117856,
          x2: 0.2025405786873677,
          y1: 0.10518518518518519,
          y2: 0.11654320987654321,
        },
        originalWord: "has",
      },
      {
        boundingBox: {
          x1: 0.20959774170783346,
          x2: 0.2399435426958363,
          y1: 0.10567901234567902,
          y2: 0.11703703703703704,
        },
        originalWord: "the",
      },
      {
        boundingBox: {
          x1: 0.24700070571630206,
          x2: 0.33380381086803107,
          y1: 0.10518518518518519,
          y2: 0.12,
        },
        originalWord: "following",
      },
      {
        boundingBox: {
          x1: 0.27170077628793227,
          x2: 0.32251235003528583,
          y1: 0.15555555555555556,
          y2: 0.16493827160493826,
        },
        originalWord: "Senkoo",
      },
      {
        boundingBox: {
          x1: 0.32886379675370503,
          x2: 0.3486238532110092,
          y1: 0.15901234567901235,
          y2: 0.16493827160493826,
        },
        originalWord: "wa",
      },
      {
        boundingBox: {
          x1: 0.39378969654199014,
          x2: 0.41778405081157377,
          y1: 0.15901234567901235,
          y2: 0.16493827160493826,
        },
        originalWord: "nan",
      },
      {
        boundingBox: {
          x1: 0.42413549752999297,
          x2: 0.45589273112208895,
          y1: 0.15604938271604937,
          y2: 0.1654320987654321,
        },
        originalWord: "desu",
      },
      {
        boundingBox: {
          x1: 0.2272406492589979,
          x2: 0.2427664079040226,
          y1: 0.1782716049382716,
          y2: 0.19012345679012346,
        },
        originalWord: "A",
      },
    ];
    setMappings(dummyMappings);
  }, []);

  useEffect(() => {
    const image = document.getElementById("myImage") as HTMLImageElement | null;

    if (image) {
      const { width, height } = image.getBoundingClientRect();
      console.log(width, height);
      setImageDimensions({ width, height });
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
        src="oorojvmobbig64qcyfqn" // Replace with your Cloudinary image public ID or path
        alt="Etext-style image"
        width={1412}
        height={2017.854248046875}
        quality="auto"
        format="auto"
        style={{ objectFit: "contain" }}
      />

      {/* Overlay Divs */}
      {mappings.map((mapping, index) => {
        // Get normalized coordinates (x1, x2, y1, y2)
        const { x1, x2, y1, y2 } = mapping.boundingBox;

        // Convert normalized coordinates to pixel values based on image size
        const xPercentage = x1 * imageDimensions.width + 565;
        const yPercentage = y1 * imageDimensions.height;
        const widthPercentage = (x2 - x1) * imageDimensions.width; // Calculate width from x1 and x2
        const heightPercentage = (y2 - y1) * imageDimensions.height; // Calculate height from y1 and y2

        return (
          <div
            key={index}
            style={{
              position: "absolute",
              top: `${yPercentage}px`,
              left: `${xPercentage}px`,
              width: `${widthPercentage}px`,
              height: `${heightPercentage}px`,
              backgroundColor: "rgba(0, 0, 0, 0.5)", // Semi-transparent overlay
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
