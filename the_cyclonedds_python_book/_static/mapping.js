
function gen_polygon(seed, center, scale) {
    var gen = new Math.seedrandom(seed);
    const pre_angles = [...Array(10).keys()].map(i => gen.random());
    const pre_angles_sum = pre_angles.reduce((i,j) => i+j, 0) / (2 * Math.PI);
    const cumulativeSummer = (sum => value => sum += value)(0);
    const pre_angles_cumulative = pre_angles_sum.map(cumulativeSummer);
    const angles = pre_angles_cumulative.map(i => i / pre_angles_sum);
    const dist = [...Array(angles.length)].map(i => scale * (1 + gen.random()));
    const gdist = dist.map(d => d * (1 + gen.random()) / 2.0);

    function to_carthesian(r, i) { return [r * Math.cos(angles[i]) + center[0], r * Math.sin(angles[i]) + center[1]]; };
    const outer = dist.map(to_carthesian);
    const inner = gdist.map(to_carthesian);
    return [outer, inner];
};

const MapDraw = {
    LAYER_BACKING = 0,
    LAYER_ISLANDS = 1,
    LAYER_BOATS = 2,
    LAYER_BORDER = 3
};

function Map() {
    self = {
        islands: [],
        boats: [],
        w: 0,
        h: 0
    };

    self.add_island = function(name, x, y, size) {
        self.islands.push({
            X: x, Y: y, size: size, name: name
        });
    };

    self.add_boat = function(name, x, y) {
        self.boats.push({
            X: x, Y: y, name: name
        });
    };

    self.draw_backing = function(canvas, ocanvas) {
        canvas.rectangle(0, 0, self.w, self.h, {roughness:0, fill: "#1271a8", bowing: 0, fillStyle: 'solid', strokeWidth: 2});
        canvas.rectangle(0, 0, self.w, self.h, {roughness:3, fill: "#1c84a0", bowing: 0, fillStyle: 'cross-hatch', strokeWidth: 2});
    };

    self.draw_islands = function(canvas, ocanvas) {
        self.islands.forEach(i => {
            var polys = gen_polygon(island.name, [island.X + self.w/2., island.Y + self.h/2.], island.size);

            canvas.polygon(polys[0], {roughness:2, fill: "#c19149", bowing: 0.4, fillStyle: 'solid', strokeWidth: 1.5});
            canvas.polygon(polys[0], {roughness:2, fill: "#a57c3e", bowing: 0.4, fillStyle: 'hachure', strokeWidth: 1.5});
            canvas.polygon(polys[1], {roughness:2, fill: "#267f08", bowing: 0.4, fillStyle: 'cross-hatch', strokeWidth: 1.1});

            ocanvas.fillStyle = "black"
            ocanvas.font = "25px \"Dancing Script\""
            ocanvas.textBaseline = "bottom"
            ocanvas.textAlign = "left"
            ocanvas.fillText(
                island.name,
                self.w/2. + island.X + island.size - 4,
                self.h/2. + island.Y - island.size - 6
            );
        });
    };

    self.draw_boats = function(canvas, ocanvas) {
        const h = 20.0;
        const w = 42.0;

        self.boats.forEach(boat => {
            const poly1_b = [[w/2 + boat.X,0 + boat.Y], [w/3 + boat.X, h/2 + boat.Y], [2*w/3 + boat.X, h/2 + boat.Y]]
            const poly2_b = [[0 + boat.X, h/2 + boat.Y], [w + boat.X, h/2 + boat.Y], [2*w/3 + boat.X, h + boat.Y], [w/3 + boat.X, h + boat.Y]]
            const poly3_b = [[w/2 + boat.X,h/2 + boat.Y], [w/3 + boat.X, h + boat.Y], [2*w/3 + boat.X, h + boat.Y]]

            canvas.polygon(poly1_b, {roughness:1.7, fill: "#f3f3f5", bowing: 0.6, fillStyle: 'solid', strokeWidth: 1.1});
            canvas.polygon(poly2_b, {roughness:1.7, fill: "#f3f3f5", bowing: 0.6, fillStyle: 'solid', strokeWidth: 1.1});
            canvas.curve(poly3_b, {roughness:1.7, fill: "#999999", bowing: 0.6, fillStyle: 'solid', strokeWidth: 1.1});
            canvas.curve(poly1_b, {roughness:1.7, fill: "#111111", bowing: 0.6, fillStyle: 'solid', strokeWidth: 1.1});
            canvas.curve(poly2_b, {roughness:1.7, fill: "#111111", bowing: 0.6, fillStyle: 'solid', strokeWidth: 1.1});
        });
    };

    self.draw_border = function(canvas, ocanvas) {
        canvas.rectangle(0, 0, 20, self.h, {roughness:0, fill: "#E9C181", bowing: 0, fillStyle: 'solid', strokeWidth: 2});
        canvas.rectangle(0, 0, self.w, 30, {roughness:0, fill: "#E9C181", bowing: 0, fillStyle: 'solid', strokeWidth: 2});
        canvas.rectangle(0, self.h-20, self.w, self.h, {roughness:0, fill: "#E9C181", bowing: 0, fillStyle: 'solid', strokeWidth: 2});
        canvas.rectangle(self.w-20, 0, 20, self.h, {roughness:0, fill: "#E9C181", bowing: 0, fillStyle: 'solid', strokeWidth: 2});

        canvas.rectangle(20, 30, self.w-40, self.h-50, {roughness:2, fill: "#ad3c0f", bowing: 0, fillStyle: 'cross-hatch', strokeWidth: 2});

        ocanvas.fillStyle = "#873110"
        ocanvas.font = "32px \"Dancing Script\""
        ocanvas.textBaseline = "middle"
        ocanvas.textSlign = "center"
        ocanvas.fillText('The Disposed Atolls', self.w/2, 15)
    };

    self.draw = function(draw_backing, draw_islands, draw_boats, draw_border) {
        draw_backing = draw_backing ?? true;
        draw_islands = draw_islands ?? true;
        draw_boats = draw_boats ?? true;
        draw_border = draw_border ?? true;

        var ocanvas = document.getElementById('canvas-map');
        self.w = ocanvas.width;
        self.h = ocanvas.heigth;
        var canvas = rough.canvas(ocanvas, {width: self.w, height: self.h});

        if (draw_backing) self.draw_backing(canvas, ocanvas);
        if (draw_islands) self.draw_islands(canvas, ocanvas);
        if (draw_boats) self.draw_boats(canvas, ocanvas);
        if (draw_border) self.draw_border(canvas, ocanvas);
    };

    return self;
}