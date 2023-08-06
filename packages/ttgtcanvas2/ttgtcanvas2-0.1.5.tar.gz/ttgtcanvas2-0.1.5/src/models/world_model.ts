import Konva from 'konva';
import { RobotModel } from './robot_model';
import $ from 'jquery';
import _isNumber from 'lodash/isNumber';
import _random from 'lodash/random';
import _padStart from 'lodash/padStart';

const walls_config: { [key: string]: any } = {
  normal: {
    x: 50,
    y: 25,
    stroke: 'darkred',
    strokeWidth: 10,
  },

  removable: {
    x: 50,
    y: 25,
    stroke: '#de1738',
    strokeWidth: 10,
  },

  goal: {
    x: 50,
    y: 25,
    stroke: 'darkred',
    strokeWidth: 7,
    dash: [10, 10],
  },
};
export class WorldModel {
  rows: number;
  cols: number;
  vwalls: any;
  hwalls: any;
  robots: any;
  width: number;
  height: number;
  bs: number;
  objects: any;
  tileMap: any;
  tiles: any;
  ui: {
    wrapper: HTMLDivElement;
    stage?: Konva.Stage;
    layers: {
      main: Konva.Layer;
      line: Konva.Layer;
      msg: Konva.Layer;
      bg: Konva.Layer;
    };
  };

  constructor() {
    this.init_ui();
  }

  init(
    rows: number,
    cols: number,
    vwalls = [],
    hwalls = [],
    robots = [],
    objects = {},
    tileMap = {},
    tiles = []
  ) {
    this.rows = rows;
    this.cols = cols;
    this.vwalls = vwalls;
    this.hwalls = hwalls;
    this.bs = 50; //box_size
    this.height = rows * this.bs;
    this.width = cols * this.bs;
    this.objects = objects;
    this.tileMap = tileMap;
    this.tiles = tiles;
    this.draw_canvas();

    this.robots = robots.map(
      (robot: RobotModel, i: number) =>
        new RobotModel(
          i,
          this,
          robot.x,
          robot.y,
          robot.orientation,
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
        bg: new Konva.Layer(),
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

    stage.add(this.ui.layers.bg);
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

  draw_custom(obj_name: string, x: number, y: number, val: number) {
    let imagePath = this.tileMap[obj_name];
    let [cx, cy] = this.point2cxy(x + 1, y);
    Konva.Image.fromURL(imagePath, (node: Konva.Image) => {
      node.setAttrs({
        x: cx + 5,
        y: cy - 25,
        width: 40,
        height: 40,
        name: `obj-${x}-${y}-img`,
      });
      this.ui.layers.main.add(node);
      this.ui.layers.main.batchDraw();
    });

    let num = new Konva.Text({
      text: `${val}`,
      x: cx + 32,
      y: cy + 2,
      fontSize: 16,
      name: `obj-${x}-${y}-text`,
    });
    this.ui.layers.main.add(num);
  }

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
    this.draw_tiles();
  }

  _draw_tile(x: number, y: number, tile: string) {
    let [cx, cy] = this.point2cxy(x, y);
    let imagePath = this.tileMap[tile];
    Konva.Image.fromURL(imagePath, (node: Konva.Image) => {
      node.setAttrs({
        x: cx + 50,
        y: cy - 25,
        width: 50,
        height: 50,
        name: `obj-${x}-${y}-tilebg`,
      });
      this.ui.layers.bg.add(node);
      this.ui.layers.bg.batchDraw();
    });
  }

  draw_tiles() {
    this.tiles.forEach((list: any, row: number) => {
      list.forEach((tile: any, col: number) => {
        if (!!tile) {
          this._draw_tile(row + 1, col + 1, tile);
        }
      });
    });
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

  draw_wall(x: number, y: number, dir: string, wall_type: string = 'normal') {
    let config = walls_config[wall_type];
    let border = null;
    let [cx, cy] = this.point2cxy(x, y);
    if (dir === 'east') {
      border = new Konva.Line({
        ...config,
        name: `vwall-${x}-${y}`,
        points: [cx + this.bs, cy - this.bs, cx + this.bs, cy],
      });
    }

    if (dir === 'north') {
      border = new Konva.Line({
        name: `hwall-${x}-${y}`,
        ...config,
        points: [cx, cy - this.bs, cx + this.bs, cy - this.bs],
      });
    }

    if (border) this.ui.layers.main.add(border);
  }

  remove_wall(x: number, y: number, dir: string) {
    if (dir !== 'north' && dir !== 'east') return;
    let wall = this.ui.layers.main.find(
      `.${dir === 'north' ? 'hwall' : 'vwall'}-${x}-${y}`
    )[0];
    if (wall) {
      wall.destroy();
    }
    this.ui.layers.main.draw();
  }

  draw_typed_wall(x: number, y: number, dir: string, val: number) {
    let [isGoal, isRemovable, isWall] = _padStart(
      Number(val).toString(2),
      3,
      '0'
    );

    if (parseInt(isWall)) {
      if (parseInt(isRemovable)) {
        this.draw_wall(x, y, dir, 'removable');
      } else {
        this.draw_wall(x, y, dir, 'normal');
      }
    } else if (parseInt(isGoal)) {
      this.draw_wall(x, y, dir, 'goal');
    }
  }

  draw_walls() {
    this.hwalls.forEach((hw: any, i: number) => {
      hw.forEach((val: number, j: number) => {
        if (val) {
          this.draw_typed_wall(i, j, 'north', val);
        } else {
          this.remove_wall(i, j, 'north');
        }
      });
    });

    this.vwalls.forEach((vw: any, i: number) => {
      vw.forEach((val: number, j: number) => {
        if (val) {
          this.draw_typed_wall(i, j, 'east', val);
        } else {
          this.remove_wall(i, j, 'east');
        }
      });
    });
  }
}
