import { app } from "../../../scripts/app.js";
import { ComfyWidgets } from "../../../scripts/widgets.js";

// Register ShowTextNode
app.registerExtension({
    name: "ComfyUI.PromptTranslator.ShowTextNode",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "ShowTextNode") {
            // On node created
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function () {
                const r = onNodeCreated?.apply(this, arguments);

                // Add a text widget to display the content
                const widget = ComfyWidgets.STRING(
                    this,
                    "output_text",
                    ["STRING", { multiline: true }],
                    app
                );
                widget.widget.inputEl.readOnly = true;
                widget.widget.inputEl.style.opacity = "1";
                this.textWidget = widget.widget;

                return r;
            };

            function populate(text) {
				if (this.widgets) {
					// On older frontend versions there is a hidden converted-widget
					const isConvertedWidget = +!!this.inputs?.[0].widget;
					for (let i = isConvertedWidget; i < this.widgets.length; i++) {
						this.widgets[i].onRemove?.();
					}
					this.widgets.length = isConvertedWidget;
				}

				const v = [...text];
				if (!v[0]) {
					v.shift();
				}
				for (let list of v) {
					// Force list to be an array, not sure why sometimes it is/isn't
					if (!(list instanceof Array)) list = [list];
					for (const l of list) {
						const w = ComfyWidgets["STRING"](this, "text_" + this.widgets?.length ?? 0, ["STRING", { multiline: true }], app).widget;
						w.inputEl.readOnly = true;
						w.inputEl.style.opacity = 0.6;
						w.value = l;
					}
				}

				requestAnimationFrame(() => {
					const sz = this.computeSize();
					if (sz[0] < this.size[0]) {
						sz[0] = this.size[0];
					}
					if (sz[1] < this.size[1]) {
						sz[1] = this.size[1];
					}
					this.onResize?.(sz);
					app.graph.setDirtyCanvas(true, false);
				});
			}
            
            // On executed - update the text display
            const onExecuted = nodeType.prototype.onExecuted;
            nodeType.prototype.onExecuted = function (message) {
                onExecuted?.apply(this, arguments);
                populate.call(this, message.text);
            };
        }
    },
});
