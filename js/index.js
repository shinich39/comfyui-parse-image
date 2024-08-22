"use strict";

import { app } from "../../../scripts/app.js";
import { api } from "../../../scripts/api.js";
import { loadMetadata } from "./libs/workflow-editor.js";

const PARSER_TYPES = [
  "LoadBooleanFromImage",
  "LoadIntFromImage",
  "LoadFloatFromImage",
  "LoadStringFromImage",
  "LoadComboFromImage",
];

const IMAGE_LOADER_TYPES = [
  "LoadImage",
  "LoadImage //Inspire",
  "Load image with metadata [Crystools]",
  "Image Load",
  "PutImage",
];

function initNode() {
  try {
    if (this.statics && this.statics.isInitialized) {
      return;
    }

    const self = this;

    this.statics = {
      isInitialized: false,
    };

    this.statics.getImageNode = (function() {
      let input = this.inputs?.find(e => ["pixels", "image"].indexOf(e.name) > -1);
      if (!input || !input.link) {
        return;
      }
      let linkId = input.link;
      let link = app.graph.links.find(e => e && e.id === linkId);
      let targetId = link.origin_id;
      let target = app.graph._nodes.find(e => e.id === targetId);
      while(target && IMAGE_LOADER_TYPES.indexOf(target.comfyClass) === -1) {
        input = target.inputs?.find(e => ["pixels", "image"].indexOf(e.name) > -1);
        if (!input || !input.link) {
          return;
        }
        linkId = input.link;
        link = graph.links.find(e => e && e.id === linkId);
        targetId = link.origin_id;
        target = app.graph._nodes.find(e => e.id === targetId);
      }
      return target;
    }).bind(this);

    this.statics.getMetadata = (async function() {
      const node = this.statics.getImageNode();
      if (!node) {
        return;
      }
      if (node.parsedData) {
        return node.parsedData;
      }
      const filePath = getFilePath(node);
      if (!filePath) {
        return;
      }
      try {
        const { width, height, info, format } = await loadMetadata(filePath);
        let prompt = JSON.parse(info.prompt);
        let workflow = JSON.parse(info.workflow);
        let nodes = Object.entries(prompt).map(e => {
          const id = parseInt(e[0]);
          const type = e[1].class_type;
          const values = e[1].inputs;
          const node = workflow.nodes.find(n => n.id === id);
          let title = node.title;
          if (!title && LiteGraph.registered_node_types[type]) {
            const n = LiteGraph.registered_node_types[type];
            title = n.title;
          }
          return {
            id,
            title,
            type,
            values,
          }
        }).sort((a, b) => a.id - b.id);

        node.parsedData = {
          width,
          height,
          nodes,
          prompt,
          workflow,
        }

        return node.parsedData;
      } catch(err) {
        console.error(err);
      }
    }).bind(this);

    setTimeout(() => {
      this.setSize(this.size);
      this.setDirtyCanvas(true, true);
    }, 128);

    this.statics.isInitialized = true;
  } catch(err) {
    console.error(err);
  }
}

function getFilePath(node) {
  if (node && node.widgets) {
    switch(node.type) {
      // core
      case "LoadImage": return `ComfyUI/input/${node.widgets.find(e => e.name === "image").value}`;
      // ComfyUI-Inspire-Pack
      case "LoadImage //Inspire": return `ComfyUI/input/${node.widgets.find(e => e.name === "image").value}`;
      // ComfyUI-Crystools
      case "Load image with metadata [Crystools]": return `ComfyUI/input/${node.widgets.find(e => e.name === "image").value}`;
      // WAS Node Suite
      case "Image Load": return `${node.widgets.find(e => e.name === "image_path").value}`;
      // comfyui-put-image
      case "PutImage": return `${node.widgets.find(e => e.name === "dir_path").value}/${node.widgets.find(e => e.name === "filename").value}`;
    }
  }
}

function matchNode(n, q) {
  if (!n || !q) {
    return false;
  }
  if (n.title && n.title === q) {
    return true;
  }
  if (n.type && n.type === q) {
    return true;
  }
  if (n.id && n.id == q) {
    return true;
  }
  return false;
}

function findNode(nodes, query, reverse) {
  if (!reverse) {
    for (let i = 0; i < nodes.length; i++) {
      if (matchNode(nodes[i], query)) {
        return nodes[i];
      }
    }
  } else {
    for (let i = nodes.length - 1; i >= 0; i--) {
      if (matchNode(nodes[i], query)) {
        return nodes[i];
      }
    }
  }
}

app.registerExtension({
	name: `shinich39.ParseImage`,
  setup() {

    // render before start a new queue
    const origQueuePrompt = app.queuePrompt;
    app.queuePrompt = async function(number, batchCount) {

      // reset
      for (const node of app.graph._nodes) {
        if (IMAGE_LOADER_TYPES.indexOf(node.comfyClass) > -1) {
          delete node.parsedData;
        }
      }

      // render
      for (const node of app.graph._nodes) {
        if (PARSER_TYPES.indexOf(node.comfyClass) > -1) {
          try {
            const { width, height, nodes, workflow, prompt } = await node.statics.getMetadata();
            const q = node.widgets[0];
            const v = node.widgets[1];

            if (q.value === "width") {
              v.value = width;
            } else if (q.value === "height") {
              v.value = height;
            } else {
              const qv = q.value.split(".");
              const nn = qv.slice(0, qv.length - 1).join(".");
              const wn = qv.slice(qv.length - 1).join(".");
    
              const n = findNode(nodes, nn);
              if (n && n.values[wn]) {
                v.value = n.values[wn];
              }
            }
          } catch(err) {
            console.error(err);
          }
        }
      }

      const r = await origQueuePrompt.apply(this, arguments);
      return r;
    }
  },
  async afterConfigureGraph(missingNodeTypes) {
    for (const node of app.graph._nodes) {
      if (PARSER_TYPES.indexOf(node.comfyClass) > -1) {
        initNode.apply(node);
      }
    }
	},
  nodeCreated(node) {
    if (PARSER_TYPES.indexOf(node.comfyClass) > -1) {
      initNode.apply(node);
    }
  },
});