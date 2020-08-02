/** @jsx jsx */
import { jsx } from "@emotion/core";
import React, { useEffect, useState } from "react";
import { PieChart, Pie, Sector, Cell } from "recharts";
import { getChartData } from "./api";

const renderActiveShape = (props: any) => {
  const RADIAN = Math.PI / 180;
  const {
    cx,
    cy,
    midAngle,
    innerRadius,
    outerRadius,
    startAngle,
    endAngle,
    fill,
    payload,
    percent,
    value,
  } = props;
  const sin = Math.sin(-RADIAN * midAngle);
  const cos = Math.cos(-RADIAN * midAngle);
  const sx = cx + (outerRadius + 10) * cos;
  const sy = cy + (outerRadius + 10) * sin;
  const mx = cx + (outerRadius + 30) * cos;
  const my = cy + (outerRadius + 30) * sin;
  const ex = mx + (cos >= 0 ? 1 : -1) * 22;
  const ey = my;
  const textAnchor = cos >= 0 ? "start" : "end";

  return (
    <g>
      <Sector
        cx={cx}
        cy={cy}
        innerRadius={innerRadius}
        outerRadius={outerRadius}
        startAngle={startAngle}
        endAngle={endAngle}
        fill={fill}
      />
      <Sector
        cx={cx}
        cy={cy}
        startAngle={startAngle}
        endAngle={endAngle}
        innerRadius={outerRadius + 6}
        outerRadius={outerRadius + 10}
        fill={fill}
      />
      <path
        d={`M${sx},${sy}L${mx},${my}L${ex},${ey}`}
        stroke={fill}
        fill="none"
      />
      <circle cx={ex} cy={ey} r={2} fill={fill} stroke="none" />
      <text
        x={ex + (cos >= 0 ? 1 : -1) * 12}
        y={ey}
        textAnchor={textAnchor}
        fill="#333"
      >{`${payload.name} ${value}`}</text>
      <text
        x={ex + (cos >= 0 ? 1 : -1) * 12}
        y={ey}
        dy={18}
        textAnchor={textAnchor}
        fill="#999"
      >
        {`${(percent * 100).toFixed(2)}%`}
      </text>
    </g>
  );
};

const COLORS = ["#00897b", "#d32f2f"];

interface Props {
  command?: string;
}

export const Chart: React.FC<Props> = ({ command }) => {
  const [chartData, setChartData] = useState<{ name: string; value: number }[]>(
    []
  );

  const [activeIndex, setActiveIndex] = useState<number>(0);

  useEffect(() => {
    async function loadData() {
      // TODO: create api
      //   const data = await getChartData(command);
      //   setChartData([
      //     {
      //       name: "Позитивные",
      //       value: data.positive,
      //     },
      //     {
      //       name: "Негативные",
      //       value: data.negative,
      //     },
      //   ]);
      setChartData([
        {
          name: "Позитивные",
          value: 900,
        },
        {
          name: "Негативные",
          value: 500,
        },
      ]);
    }

    loadData();
  }, [command]);

  function onPieEnter(data: any, index: any) {
    setActiveIndex(index);
  }

  return (
    <PieChart width={500} height={400}>
      <Pie
        activeIndex={activeIndex}
        activeShape={renderActiveShape}
        data={chartData}
        dataKey="value"
        nameKey="name"
        cx="50%"
        cy="50%"
        innerRadius={0}
        outerRadius={80}
        fill="#82ca9d"
        onMouseEnter={onPieEnter}
      >
        {chartData.map((entry, index) => (
          <Cell fill={COLORS[index % COLORS.length]} />
        ))}
      </Pie>
    </PieChart>
  );
};
