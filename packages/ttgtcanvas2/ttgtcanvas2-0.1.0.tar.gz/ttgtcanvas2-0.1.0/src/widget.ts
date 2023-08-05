// Copyright (c) Indresh Vishwakarma
// Distributed under the terms of the Modified BSD License.

import {
  DOMWidgetModel,
  DOMWidgetView,
  ISerializers,
} from '@jupyter-widgets/base';

import { MODULE_NAME, MODULE_VERSION } from './version';

// Import the CSS
import '../css/widget.css';
import { WorldModel } from './models/world_model';

import PQueue from 'p-queue';
const queue = new PQueue({ concurrency: 1 });

export class MazeModel extends DOMWidgetModel {
  defaults() {
    return {
      ...super.defaults(),
      _model_name: MazeModel.model_name,
      _model_module: MazeModel.model_module,
      _model_module_version: MazeModel.model_module_version,
      _view_name: MazeModel.view_name,
      _view_module: MazeModel.view_module,
      _view_module_version: MazeModel.view_module_version,
      current_call: '{}',
      method_return: '{}',
    };
  }

  static serializers: ISerializers = {
    ...DOMWidgetModel.serializers,
    // Add any extra serializers here
  };

  static model_name = 'MazeModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'MazeView'; // Set to null if no view
  static view_module = MODULE_NAME; // Set to null if no view
  static view_module_version = MODULE_VERSION;
}

export class MazeView extends DOMWidgetView {
  world_model: WorldModel;

  method_changed = () => {
    let current_call: { method_name: string; params: any; cb: any } =
      JSON.parse(this.model.get('current_call'));
    queue.add(() => {
      let ret =
        typeof this[current_call.method_name as keyof MazeView] === 'function'
          ? this[current_call.method_name as keyof MazeView].apply(
              this,
              current_call.params
            )
          : null;

      console.log('current_call in promise', current_call);
      let that = this;
      return Promise.resolve(ret).then(function (x) {
        // console.log("reached in promise");
        let data = JSON.stringify({
          value: x,
          cb: +new Date(),
          params: current_call.params,
          method: current_call.method_name,
        });
        console.log('setting return', data);
        that.model.set('method_return', data);
        that.model.save_changes();
        return data;
      });
    });
  };

  draw_all = (rows: number, cols: number, walls: number, robots = []) => {
    this.world_model.init(rows, cols, walls, robots);
  };

  render() {
    //set methods
    this.method_changed();
    this.listenTo(this.model, 'change:current_call', this.method_changed);
    if (!this.world_model) {
      this.world_model = new WorldModel();
      this.el.appendChild(this.world_model.ui.wrapper);
    }
  }
}
