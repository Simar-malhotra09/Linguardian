"use client";
import { useEffect, useState } from "react";
import katex from "katex";
import "katex/dist/katex.min.css";
import { text } from "stream/consumers";
const text = [
  [[117, 107, 176, 124], "56>>>"],
  [[182, 105, 224, 125], "会"],
  [[215, 101, 232, 136], "話"],
  [[231, 113, 234, 117], "・"],
  [[248, 105, 268, 125], "文"],
  [[272, 105, 283, 125], "法"],
  [[292, 105, 305, 125], "編"],
  [[116, 170, 144, 194], "C."],
  [[172, 171, 247, 194], "Class"],
  [[259, 171, 440, 200], "Activity—Ask"],
  [[452, 177, 513, 200], "your"],
  [[524, 171, 680, 195], "classmates"],
  [[693, 172, 759, 195], "what"],
  [[771, 172, 832, 195], "their"],
  [[845, 172, 937, 201], "majors"],
  [[950, 179, 998, 199], "are,"],
  [[1012, 172, 1062, 196], "and"],
  [[1075, 173, 1125, 196], "find"],
  [[1139, 179, 1266, 196], "someone"],
  [[171, 213, 228, 236], "who"],
  [[240, 213, 287, 236], "has"],
  [[297, 214, 340, 237], "the"],
  [[350, 213, 473, 243], "following"],
  [[485, 214, 566, 243], "major."],
  [[171, 282, 284, 312], "Example:"],
  [[323, 283, 438, 307], "Q:¢A"],
  [[451, 280, 533, 307], "2314"],
  [[569, 282, 580, 307], "な"],
  [[596, 281, 612, 307], "ん"],
  [[624, 284, 645, 307], "で"],
  [[649, 282, 720, 309], "すか"],
  [[699, 264, 724, 319], "。"],
  [[385, 315, 457, 334], "Senkoo"],
  [[466, 322, 494, 334], "wa"],
  [[558, 322, 592, 334], "nan"],
  [[601, 316, 646, 335], "desu"],
  [[656, 316, 682, 335], "ka."],
  [[322, 361, 344, 385], "A"],
  [[364, 364, 366, 382], ":"],
  [[406, 361, 421, 385], "に"],
  [[426, 358, 579, 387], "ほん"],
  [[483, 354, 508, 398], "ご"],
  [[507, 354, 530, 398], "で"],
  [[529, 354, 558, 398], "す"],
  [[557, 354, 582, 398], "。"],
  [[385, 394, 472, 419], "Nihongo"],
  [[480, 394, 530, 413], "desu."],
  [[598, 448, 666, 463], "name"],
  [[173, 520, 189, 540], "1."],
  [[207, 519, 313, 547], "Japanese"],
  [[170, 597, 189, 618], "2."],
  [[207, 597, 339, 618], "economics"],
  [[170, 676, 189, 697], "3."],
  [[207, 674, 299, 705], "English"],
  [[169, 755, 189, 776], "4,"],
  [[206, 753, 294, 784], "history"],
  [[170, 835, 188, 855], "5."],
  [[206, 833, 309, 855], "business"],
  [[115, 980, 141, 1003], "D."],
  [[171, 980, 231, 1003], "Role"],
  [[243, 980, 406, 1010], "Play—Using"],
  [[419, 980, 539, 1010], "Dialogue"],
  [[549, 987, 580, 1004], "as"],
  [[591, 987, 606, 1004], "a"],
  [[617, 981, 709, 1009], "model,"],
  [[722, 981, 796, 1005], "make"],
  [[806, 981, 869, 1005], "skits"],
  [[881, 981, 901, 1004], "in"],
  [[912, 982, 955, 1005], "the"],
  [[965, 982, 1088, 1011], "following"],
  [[1100, 982, 1239, 1005], "situations."],
  [[172, 1052, 188, 1072], "1."],
  [[205, 1051, 252, 1072], "You"],
  [[261, 1049, 322, 1072], "don't"],
  [[330, 1050, 386, 1073], "have"],
  [[395, 1058, 407, 1073], "a"],
  [[415, 1050, 488, 1073], "watch"],
  [[496, 1050, 551, 1073], "with"],
  [[559, 1058, 611, 1081], "you,"],
  [[620, 1051, 660, 1073], "but"],
  [[668, 1059, 714, 1081], "you"],
  [[723, 1051, 782, 1074], "need"],
  [[790, 1055, 813, 1074], "to"],
  [[822, 1051, 892, 1074], "know"],
  [[899, 1051, 959, 1074], "what"],
  [[967, 1053, 1023, 1074], "time"],
  [[1032, 1053, 1048, 1074], "it"],
  [[1057, 1053, 1081, 1074], "is."],
  [[169, 1210, 188, 1231], "2."],
  [[205, 1208, 284, 1231], "You've"],
  [[291, 1210, 337, 1239], "just"],
  [[346, 1213, 392, 1231], "met"],
  [[401, 1217, 414, 1231], "a"],
  [[422, 1210, 528, 1239], "Japanese"],
  [[537, 1217, 621, 1239], "person"],
  [[631, 1209, 676, 1232], "and"],
  [[684, 1214, 744, 1232], "want"],
  [[753, 1214, 776, 1232], "to"],
  [[785, 1214, 821, 1240], "get"],
  [[829, 1214, 853, 1232], "to"],
  [[862, 1209, 932, 1232], "know"],
  [[939, 1209, 977, 1232], "the"],
  [[985, 1217, 1076, 1240], "person."],
];

const Page = () => {
  const [ocrData, setOcrData] = useState([]);

  useEffect(() => {
    // Simulate fetching the OCR data (replace this with actual API call)
    const fetchedData = text;
    setOcrData(fetchedData);

    // Render KaTeX for LaTeX expressions
    const elements = document.querySelectorAll(".latex");
    elements.forEach((el) => {
      katex.render(el.textContent || "", el, {
        throwOnError: false,
      });
    });
  }, []);

  const renderTextWithPositions = () => {
    return ocrData.map((item, index) => {
      const [x1, y1, x2, y2] = item[0]; // Extract position coordinates
      const word = item[1]; // Extract word

      // Check if the word is LaTeX (if needed, apply a flag here based on the OCR processing)
      const isLatex = word.startsWith("\\"); // Example condition for LaTeX, customize as needed

      return isLatex ? (
        <span
          key={index}
          className="latex"
          style={{
            position: "absolute",
            left: `${x1}px`,
            top: `${y1}px`,
            fontSize: "18px",
            lineHeight: "1.6",
          }}
        >
          {`\\(${word}\\)`} {/* Render LaTeX expressions */}
        </span>
      ) : (
        <span
          key={index}
          style={{
            position: "absolute",
            left: `${x1}px`,
            top: `${y1}px`,
            fontSize: "18px",
            lineHeight: "1.6",
          }}
        >
          {word} {/* Render regular text */}
        </span>
      );
    });
  };

  return (
    <div style={{ position: "relative", padding: "20px" }}>
      <h2>Rendered OCR with LaTeX and Regular Text</h2>
      <div>{renderTextWithPositions()}</div>
    </div>
  );
};

export default Page;
