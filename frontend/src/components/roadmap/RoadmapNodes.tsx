import { Handle, NodeProps, Position } from 'reactflow';

// 透明なハンドルスタイル
const transparentHandleStyle = { opacity: 0 };

// 主要技術ノード（Primary Node）
export const PrimaryNode = ({ data }: NodeProps) => {
  return (
    <div className="px-4 py-2 shadow-md rounded-md bg-gradient-to-r from-blue-500 to-blue-700 border-2 border-blue-800 text-white min-w-[180px]">
      <Handle type="target" position={Position.Top} id="top" style={transparentHandleStyle} />
      <Handle type="target" position={Position.Right} id="right" style={transparentHandleStyle} />
      <Handle type="target" position={Position.Bottom} id="bottom" style={transparentHandleStyle} />
      <Handle type="target" position={Position.Left} id="left" style={transparentHandleStyle} />

      <div className="flex items-center">
        <div className="ml-2">
          <div className="text-lg font-bold">{data.label}</div>
          {/* <div className="text-xs text-blue-100">{data.description}</div> */}
        </div>
      </div>

      <Handle type="source" position={Position.Top} id="top" style={transparentHandleStyle} />
      <Handle type="source" position={Position.Right} id="right" style={transparentHandleStyle} />
      <Handle type="source" position={Position.Bottom} id="bottom" style={transparentHandleStyle} />
      <Handle type="source" position={Position.Left} id="left" style={transparentHandleStyle} />
    </div>
  );
};

// 基本スキルノード（Secondary Node）
export const SecondaryNode = ({ data, selected }: NodeProps) => {
  return (
    <div
      className={`px-4 py-2 rounded-md shadow-md text-center ${selected ? 'ring-2 ring-blue-500' : ''}`}
      style={{ background: '#ffe082', minWidth: '150px' }}
    >
      <Handle type="target" position={Position.Top} id="top" style={transparentHandleStyle} />
      <Handle type="target" position={Position.Right} id="right" style={transparentHandleStyle} />
      <Handle type="target" position={Position.Bottom} id="bottom" style={transparentHandleStyle} />
      <Handle type="target" position={Position.Left} id="left" style={transparentHandleStyle} />

      <div className="font-medium">{data.label}</div>

      <Handle type="source" position={Position.Top} id="top" style={transparentHandleStyle} />
      <Handle type="source" position={Position.Right} id="right" style={transparentHandleStyle} />
      <Handle type="source" position={Position.Bottom} id="bottom" style={transparentHandleStyle} />
      <Handle type="source" position={Position.Left} id="left" style={transparentHandleStyle} />
    </div>
  );
};

// 推奨スキルノード（Recommended Node）
export const RecommendedNode = ({ data, selected }: NodeProps) => {
  return (
    <div
      className={`px-4 py-2 rounded-md shadow-md text-center ${selected ? 'ring-2 ring-blue-500' : ''}`}
      style={{ background: '#c8e6c9', minWidth: '150px' }}
    >
      <Handle type="target" position={Position.Top} id="top" style={transparentHandleStyle} />
      <Handle type="target" position={Position.Right} id="right" style={transparentHandleStyle} />
      <Handle type="target" position={Position.Bottom} id="bottom" style={transparentHandleStyle} />
      <Handle type="target" position={Position.Left} id="left" style={transparentHandleStyle} />

      <div className="font-medium">{data.label}</div>

      <Handle type="source" position={Position.Top} id="top" style={transparentHandleStyle} />
      <Handle type="source" position={Position.Right} id="right" style={transparentHandleStyle} />
      <Handle type="source" position={Position.Bottom} id="bottom" style={transparentHandleStyle} />
      <Handle type="source" position={Position.Left} id="left" style={transparentHandleStyle} />
    </div>
  );
};

// オプションノード（Optional Node）
export const OptionalNode = ({ data, selected }: NodeProps) => {
  return (
    <div
      className={`px-4 py-2 rounded-md shadow-md text-center ${selected ? 'ring-2 ring-blue-500' : ''}`}
      style={{ background: '#ddd', minWidth: '150px' }}
    >
      <Handle type="target" position={Position.Top} id="top" style={transparentHandleStyle} />
      <Handle type="target" position={Position.Right} id="right" style={transparentHandleStyle} />
      <Handle type="target" position={Position.Bottom} id="bottom" style={transparentHandleStyle} />
      <Handle type="target" position={Position.Left} id="left" style={transparentHandleStyle} />

      <div className="font-medium">{data.label}</div>

      <Handle type="source" position={Position.Top} id="top" style={transparentHandleStyle} />
      <Handle type="source" position={Position.Right} id="right" style={transparentHandleStyle} />
      <Handle type="source" position={Position.Bottom} id="bottom" style={transparentHandleStyle} />
      <Handle type="source" position={Position.Left} id="left" style={transparentHandleStyle} />
    </div>
  );
};

// ノードタイプをエクスポート
export const nodeTypes = {
  primary: PrimaryNode,
  secondary: SecondaryNode,
  recommended: RecommendedNode,
  optional: OptionalNode,
};
