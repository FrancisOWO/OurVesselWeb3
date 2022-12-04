
// let map = new BMapGL.Map("allmap");		// 创建Map实例

// 根据id查找覆盖物
function findOverlayByID(map, id) {
	let allOverlay = map.getOverlays();
	for(let i = 0; i < allOverlay.length; i++){
		// id属性存在 且 ==id
		if (allOverlay[i].id && allOverlay[i].id == id) {
			return allOverlay[i];
		}
	}
	return false;
}

// 根据id删除覆盖物
function removeOverlayByID(map, id) {
	let overlay = findOverlayByID(map, id);
	if(overlay == false)	// 没找到
		return false;
	// 找到overlay，移除
	map.removeOverlay(overlay);
	return true;
}

function mapCenterAndZoom(map, lng, lat, zoom) {
	map.centerAndZoom(new BMapGL.Point(lng, lat), zoom);
}

function getMarkerIcon(shape, color, scale) {
	// 各种定位图标 allStyleMarker.png
	// 形状：球针，同心圆，旗
	// 宽高：(10,20)，(18,30)，(16,18)
	// 颜色：绿，蓝，红，黄，紫，粉
	let iconPath = "/static/images/allStyleMarker.png";
	let img_w = 144, img_h = 92;

	let icon_w = [10, 18, 16];
	let icon_h = [22, 26, 18];
	let icon_hsum = [0, 22, 48];

	// 缩放计算
	let icon_ws = scale*icon_w[shape], icon_hs = scale*icon_h[shape], icon_hsums = scale*icon_hsum[shape];

	let iconSize = new BMapGL.Size(icon_ws, icon_hs);
	let iconTemp = new BMapGL.Icon(iconPath, iconSize, {
		// 图标相对鼠标点击的位置
		"anchor": new BMapGL.Size(icon_ws/2, icon_hs),
		// 图标在allStyleMarker.png中的位置
		"imageOffset": new BMapGL.Size(color*icon_ws, icon_hsums)
	});
	// 缩放图片大小
	iconTemp.setImageSize(new BMapGL.Size(scale*img_w, scale*img_h));

	return iconTemp;
}

// 在当前位置添加标注
function markCurrentPoint(map, lng, lat, label) {

	// 当前点：红色 同心圆
	let shape = 1; color = 2, scale = 1.2;
	let iconCur = getMarkerIcon(shape, color, scale);

	// 若标注已存在则移除
	let m_cur_id = "m_cur";
	removeOverlayByID(map, m_cur_id);

	let p_cur = new BMapGL.Point(lng, lat);
	// 当前位置标注
	let m_cur = new BMapGL.Marker(p_cur, {
		"enableDragging": false,
		"icon": iconCur
	});
	m_cur.id = m_cur_id;
	
	m_cur.setLabel(new BMapGL.Label(label));
	map.addOverlay(m_cur);			// 在地图上添加标注
}


function showBMap(map){

	// GL版命名空间为BMapGL
    // 按住鼠标右键，修改倾斜角和角度
	let p_center = new BMapGL.Point(106, 34);
	map.centerAndZoom(p_center, 4);			// 初始化地图,设置中心点坐标和地图级别
	map.enableScrollWheelZoom(true);		// 开启鼠标滚轮缩放

	// 监听鼠标点击
	let p_click = p_center;	 // new BMapGL.Point(0, 0);
	map.addEventListener('rightclick', function(e) {
		p_click.lng = e.latlng.lng;
		p_click.lat = e.latlng.lat;
	});

	// 各种定位图标 allStyleMarker.png
	// 形状：球针，同心圆，旗
	// 宽高：(10,20)，(18,30)，(16,18)
	// 颜色：绿，蓝，红，黄，紫，粉
	let iconPath = "/static/images/allStyleMarker.png";
	let icon_w = [10, 18, 16];
	let icon_h = [22, 27, 18];
	let icon_hsum = [0, 22, 49];

	// 起点：蓝色 同心圆
	let shape = 1, color = 1, scale = 1.2;
	// let iconCircSize = new BMapGL.Size(icon_w[shape], icon_h[shape]);
	// let iconFrom = new BMapGL.Icon(iconPath, iconCircSize, {
	// 	// 图标相对鼠标点击的位置
	// 	"anchor": new BMapGL.Size(icon_w[shape]/2, icon_h[shape]),
	// 	// 图标在allStyleMarker.png中的位置
	// 	"imageOffset": new BMapGL.Size(color*icon_w[shape], icon_hsum[shape])
	// });
	// iconFrom.setImageSize(scale*icon_w[shape], scale*icon_h[shape]);
	iconFrom = getMarkerIcon(shape, color, scale);

	// 终点：红色 同心圆
	color = 2;
	iconTo = getMarkerIcon(shape, color, scale);
	// let iconTo = new BMapGL.Icon(iconPath, iconCircSize, {
	// 	"anchor": new BMapGL.Size(icon_w[shape]/2, icon_h[shape]),
	// 	"imageOffset": new BMapGL.Size(color*icon_w[shape], icon_hsum[shape])
	// });
	// iconTo.setImageSize(scale*icon_w[shape], scale*icon_h[shape]);


	let m_from_id = "m_from";
	let m_to_id = "m_to";

	// 起点 终点坐标
	let p_from = p_center;
	let p_to = p_center;

	// 画出路线	// TODO: 路线规划
	let track_id = "track";
	function drawTrack(p1, p2){
		let track = new BMapGL.Polyline([
				p1,
				p2
			], {strokeColor:"green", strokeWeight:2, strokeOpacity:0.5});
		track.id = track_id;
		map.addOverlay(track);
	}

	// 定义右键菜单
	let txtMenuItem = [
	        {
	            text:"放大",					// 定义菜单项的显示文本
	            callback: function () {		// 定义菜单项点击触发的回调函数
	                map.zoomIn();
	            }
	        },
	        {
	            text:"缩小",
	            callback: function () {
	                map.zoomOut();
	            }
	        },
	        {
	        	text:"设为起点",
	        	callback: function() {
	        		// 若标注、轨迹已存在则移除
	        		removeOverlayByID(map, m_from_id);
	        		removeOverlayByID(map, track_id);

					// 起点标注
					let m_from = new BMapGL.Marker(p_click, {
						"enableDragging": true,
						"icon": iconFrom
					});
					m_from.id = m_from_id;
					
					m_from.setLabel(new BMapGL.Label("起点"));
					map.addOverlay(m_from);			// 在地图上添加标注

					p_from =  m_from.getPosition();
					// alert('【起点】经纬度：' + p_from.lng + ', ' + p_from.lat);

					// 终点存在，则画线
					if(findOverlayByID(map, m_to_id) != false)
						drawTrack(p_from, p_to);
	        	}
	        },
	        {
	        	text:"设为终点",
	        	callback: function() {
	        		// 若标注、轨迹已存在则移除
	        		removeOverlayByID(map, m_to_id);
	        		removeOverlayByID(map, track_id);

					// 终点标注
					let m_to = new BMapGL.Marker(p_click, {
						"enableDragging": true,
						"icon": iconTo
					});
					m_to.id = m_to_id;
					
					m_to.setLabel(new BMapGL.Label("终点"));
					map.addOverlay(m_to);			// 在地图上标注

					p_to =  m_to.getPosition();
					// alert('【终点】经纬度：' + p_to.lng + ', ' + p_to.lat);

					// 起点存在，则画线
					if(findOverlayByID(map, m_from_id) != false)
						drawTrack(p_from, p_to);
	        	}
	        },
	    ];

	let menu = new BMapGL.ContextMenu();
	for(let i = 0; i < txtMenuItem.length; i++){
	    menu.addItem(new BMapGL.MenuItem(	// 定义菜单项实例
	        txtMenuItem[i].text,			// 传入菜单项的显示文本
	        txtMenuItem[i].callback,		// 传入菜单项的回调函数
	        {
	            width: 100,					// 指定菜单项的宽度
	            id: 'menu' + i				// 指定菜单项dom的id
	        }
	    ));
	}

	// 给地图添加右键菜单
	map.addContextMenu(menu);
}

function hoverElementByID(id) {
    // 标记是拖曳还是点击
    let oDiv = document.getElementById(id);
    let beforeX, beforeY; // div的坐标
    let startX, startY; // 鼠标点击的坐标

    let move = false;

    oDiv.addEventListener('mousedown', function (e) {
        let ev = e || event;
        move = true;

        beforeX = this.offsetLeft;
        beforeY = this.offsetTop;

        ev.preventDefault();

        // 鼠标按下时的坐标
        startX = ev.clientX;
        startY = ev.clientY;
    });

    const Xmax = document.documentElement.clientWidth - this.offsetWidth;
    const Ymax = document.documentElement.clientHeight - this.offsetHeight;
    oDiv.addEventListener('mousemove', function (e) {
        if (move != true)
           return;

        let ev = e || event;

        // 移动后div左上角坐标 (Left,Top)
        let L = ev.clientX - startX + beforeX;
        let T = ev.clientY - startY + beforeY;

        // 限制拖拽的X范围，不能拖出屏幕
        if (L < 0) {
            L = 0;
        } else if (L > Xmax) {
            L = Xmax;
        }
        // 限制拖拽的Y范围，不能拖出屏幕
        if (T < 0) {
            T = 0;
        } else if (T > Ymax) {
            T = Ymax;
        }
        // 改变 div 位置
        this.style.left = L + 'px';
        this.style.top = T + 'px';
    });

    oDiv.addEventListener('mouseup', function () {
        move = false;
    });
}
