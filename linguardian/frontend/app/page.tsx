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
  const [visibleWords, setVisibleWords] = useState<boolean[]>([]); // Moved useState here
  const [imageDimensions, setImageDimensions] = useState<{
    width: number;
    height: number;
    x: number;
  }>({
    width: 0,
    height: 0,
    x: 0,
  });

  useEffect(() => {
    const dummyMappings: Mapping[] = [
      {
        boundingBox: {
          x1: 0.1460832745236415,
          x2: 0.2562962962962963,
          y1: 0.2208892025405787,
          y2: 0.27012345679012345,
        },
        originalWord: "Japanese",
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
    ];

    // Set the mappings and visibleWords arrays
    setMappings(dummyMappings);
    setVisibleWords(new Array(dummyMappings.length).fill(false)); // Update state here
  }, []);

  const toggleVisibility = (index: number) => {
    setVisibleWords((prev) =>
      prev.map((visible, i) => (i === index ? !visible : visible))
    );
  };

  // Log visibleWords outside the useEffect for debugging
  console.log(visibleWords);

  useEffect(() => {
    const image = document.getElementById("myImage") as HTMLImageElement | null;

    if (image) {
      const updateDimensions = () => {
        const rect = image.getBoundingClientRect();
        const { x, width, height } = rect;
        setImageDimensions({ x, width, height });
      };

      updateDimensions();

      const resizeObserver = new ResizeObserver(() => {
        updateDimensions();
      });

      const mutationObserver = new MutationObserver(() => {
        updateDimensions();
      });

      resizeObserver.observe(image);
      mutationObserver.observe(image, {
        attributes: true,
        attributeFilter: ["style"],
      });

      return () => {
        resizeObserver.disconnect();
        mutationObserver.disconnect();
      };
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
        src="oorojvmobbig64qcyfqn"
        alt="Etext-style image"
        width={1412}
        height={2017.854248046875}
        quality="auto"
        format="auto"
        style={{ objectFit: "contain" }}
      />

      {/* Overlay Divs */}
      {mappings.map((mapping, index) => {
        const { x1, x2, y1, y2 } = mapping.boundingBox;
        const xPercentage = x1 * imageDimensions.width + imageDimensions.x;
        const yPercentage = y1 * imageDimensions.height;
        const widthPercentage = (x2 - x1) * imageDimensions.width;
        const heightPercentage = (y2 - y1) * imageDimensions.height;

        return (
          <div
            key={index}
            onClick={() => toggleVisibility(index)}
            style={{
              position: "absolute",
              top: `${yPercentage}px`,
              left: `${xPercentage}px`,
              width: `${widthPercentage}px`,
              height: `${heightPercentage}px`,
              backgroundColor: "rgba(1000, 0, 0, 0.5)",
              backdropFilter: "blur(10px)",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              border: "2px solid red",
              cursor: "pointer", // Add cursor pointer to indicate it's clickable
            }}
          >
            {visibleWords[index] && (
              <span style={{ color: "black", fontWeight: "bold" }}>
                {mapping.originalWord}
              </span>
            )}
          </div>
        );
      })}
    </div>
  );
}
