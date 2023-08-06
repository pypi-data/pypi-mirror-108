import Konva from 'konva';
import { RobotModel } from './robot_model';
import $ from 'jquery';
import _isNumber from 'lodash/isNumber';
import _random from 'lodash/random';
export class WorldModel {
  rows: number;
  cols: number;
  walls: any;
  robots: any;
  width: number;
  height: number;
  bs: number;
  objects: any;
  ui: {
    wrapper: HTMLDivElement;
    stage?: Konva.Stage;
    layers: {
      main: Konva.Layer;
      line: Konva.Layer;
      msg: Konva.Layer;
    };
  };

  constructor() {
    this.init_ui();
  }

  init(rows: number, cols: number, walls = {}, robots = [], objects = {}) {
    this.rows = rows;
    this.cols = cols;
    this.walls = walls;
    this.bs = 50; //box_size
    this.height = rows * this.bs;
    this.width = cols * this.bs;
    this.objects = objects;
    this.draw_canvas();

    this.robots = robots.map(
      (robot: RobotModel, i: number) =>
        new RobotModel(
          i,
          this,
          robot.x,
          robot.y,
          robot._orientation,
          robot.image
        )
    );

    console.log(robots);

    this.robots[0].draw();
  }

  init_ui() {
    let wrapper = document.createElement('div');
    wrapper.setAttribute('class', 'ttgt-wrapper');

    let elem = document.createElement('div');
    elem.setAttribute('id', 'container');

    let bttnTxt = document.createElement('span');
    let txtNode = document.createTextNode('Toggle');
    bttnTxt.appendChild(txtNode);
    bttnTxt.setAttribute('class', 'bttn-txt');

    let sidebar = document.createElement('button');
    sidebar.appendChild(bttnTxt);
    sidebar.setAttribute('class', 'ttgt-sidebar-bttn');
    sidebar.onclick = function () {
      $('#container').toggle();
    };

    wrapper.appendChild(elem);
    wrapper.appendChild(sidebar);

    this.ui = {
      wrapper,
      layers: {
        main: new Konva.Layer(),
        line: new Konva.Layer(),
        msg: new Konva.Layer(),
      },
    };
  }

  draw_canvas() {
    let padding = 25;
    let stage = new Konva.Stage({
      container: 'container',
      width: this.width + this.bs + padding,
      height: this.height + this.bs + padding,
    });

    stage.add(this.ui.layers.main);
    stage.add(this.ui.layers.line);
    stage.add(this.ui.layers.msg);
    this.ui.stage = stage;

    //draw stage
    this.draw_border();
    this.draw_grid();
    this.draw_objects();

    this.ui.layers.main.draw();
  }

  draw_objects() {
    for (const key in this.objects) {
      const [x, y] = key.split(',').map((zz) => parseInt(zz));
      this.draw_object(x, y, this.objects[key]);
    }
  }

  draw_object(x: number, y: number, obj: any) {
    for (const obj_name in obj) {
      let val = this.parse_value(obj[obj_name]);

      if (obj_name === 'beeper') {
        this.draw_beeper(x, y, val);
      } else {
        this.draw_custom(obj_name, x, y, val);
      }
    }
  }

  update_object(x: number, y: number, val: number) {
    let text = this.ui.layers.main.find(`.obj-${x}-${y}-text`)[0];
    if (text) {
      //@ts-ignore
      text.text(`${val}`);
      this.ui.layers.main.draw();
    }
  }

  draw_beeper(x: number, y: number, val: number) {
    let radius = 0.6 * 25;
    let [cx, cy] = this.point2cxy(x + 1, y);
    cx = cx + 25;
    let circle = new Konva.Circle({
      radius: radius,
      x: cx,
      y: cy,
      fill: 'yellow',
      stroke: 'orange',
      strokeWidth: 5,
      name: `obj-${x}-${y}-circle`,
    });

    let num = new Konva.Text({
      text: `${val}`,
      x: cx - 5,
      y: cy - 7,
      fontSize: 18,
      name: `obj-${x}-${y}-text`,
    });

    this.ui.layers.main.add(circle, num);
  }

  remove_object(x: number, y: number) {
    let circle = this.ui.layers.main.find(`.obj-${x}-${y}-circle`)[0];
    let text = this.ui.layers.main.find(`.obj-${x}-${y}-text`)[0];
    let img = this.ui.layers.main.find(`.obj-${x}-${y}-img`)[0];

    if (circle) {
      //@ts-ignore
      circle.destroy();
    }
    if (text) {
      //@ts-ignore
      text.destroy();
    }
    if (img) {
      //@ts-ignore
      img.destroy();
    }
    this.ui.layers.main.draw();
  }

  draw_custom(obj_name: string, x: number, y: number, val: number) {}

  parse_value(val: number | string) {
    if (!val) return 0;
    if (_isNumber(val)) return val;
    else {
      const [min_val, max_val] = val.split('-').map((zz) => parseInt(zz));
      return _random(min_val, max_val);
    }
  }

  draw_border() {
    let box = new Konva.Rect({
      x: 50,
      y: 25,
      stroke: 'darkred',
      strokeWidth: 10,
      closed: true,
      width: this.width,
      height: this.height,
    });

    this.ui.layers.main.add(box);
  }

  draw_grid() {
    this.draw_cols();
    this.draw_rows();
    this.draw_walls();
  }

  draw_cols() {
    for (let col = 1; col < this.cols; col++) {
      let line = new Konva.Line({
        x: 50,
        y: 25,
        stroke: 'gray',
        points: [col * this.bs, 5, col * this.bs, this.height - 5],
      });

      let count = new Konva.Text({
        text: `${col}`,
        y: this.height + 40,
        x: col * this.bs + 25,
      });

      this.ui.layers.main.add(line, count);
    }

    let last_count = new Konva.Text({
      text: `${this.cols}`,
      y: this.height + 40,
      x: this.cols * this.bs + 25,
    });

    this.ui.layers.main.add(last_count);
  }

  draw_rows() {
    for (let row = 1; row < this.rows; row++) {
      let line = new Konva.Line({
        x: 50,
        y: 25,
        stroke: 'gray',
        points: [this.width - 5, row * this.bs, 5, row * this.bs],
      });

      let count = new Konva.Text({
        text: `${this.rows + 1 - row}`,
        x: 25,
        y: row * this.bs - 10,
      });

      this.ui.layers.main.add(line, count);
    }

    let last_count = new Konva.Text({
      text: `1`,
      x: 25,
      y: this.rows * this.bs - 10,
    });

    this.ui.layers.main.add(last_count);
  }

  point2cxy(x: number, y: number) {
    return [(x - 1) * this.bs, this.height - (y - 1) * this.bs];
  }

  add_wall(x: number, y: number, dir: string) {
    let border = null;
    let [cx, cy] = this.point2cxy(x, y);
    if (dir === 'east') {
      border = new Konva.Line({
        x: 50,
        y: 25,
        stroke: 'darkred',
        strokeWidth: 10,
        points: [cx + this.bs, cy - this.bs, cx + this.bs, cy],
      });
    }

    if (dir === 'north') {
      border = new Konva.Line({
        x: 50,
        y: 25,
        stroke: 'darkred',
        strokeWidth: 10,
        points: [cx, cy - this.bs, cx + this.bs, cy - this.bs],
      });
    }

    if (border) this.ui.layers.main.add(border);
  }

  draw_walls() {
    for (const coord in this.walls) {
      if (Object.prototype.hasOwnProperty.call(this.walls, coord)) {
        const walls = this.walls[coord];

        let [x, y] = coord.split(',').map((co) => parseInt(co));
        walls.map((dir: string) => {
          this.add_wall(x, y, dir);
        });
      }
    }
  }
}
