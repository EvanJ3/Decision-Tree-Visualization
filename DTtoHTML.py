from bs4 import BeautifulSoup as Soup
import pydot
import graphviz
from sklearn import tree


def WriteTree(clf, feature_names,out_file,title_string='DecisonTree',rounded=True,leaves_parallel=True,filled=True,node_ids=True,rotate=True,class_names=None):
    dot_data = tree.export_graphviz(clf, out_file=None, class_names=class_names,
                                feature_names=feature_names,  
                                rounded=rounded,leaves_parallel=leaves_parallel,
                                filled=filled,node_ids=node_ids,rotate=rotate)
    graphs = pydot.graph_from_dot_data(dot_data)
    svg_string = graphs[0].create_svg().decode('UTF-8')
    html = """
    <!DOCTYPE html>
    <html lang="en">

    <head>
      <!--  Meta  -->
      <meta charset="UTF-8">
      <title></title>
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <script src="https://cdn.jsdelivr.net/npm/svg-pan-zoom@3.5.0/dist/svg-pan-zoom.min.js"></script>
    </head>

    <style type='text/css'>



    html,
    body {
      width: 100%;
      height: 100%;
      overflow: hidden;
    }

    #mainViewContainer {
      width: 95%;
      height: 95%;
      border: 1px solid black;
      margin: 10px;
      padding: 3px;
      overflow: hidden;
    }

    #mainView {
      width: 100%;
      height: 100%;
      min-height: 100%;
    }

    .thumbViewClass {
      border: 1px solid black;
      position: absolute;
      bottom: 5px;
      left: 5px;
      width: 15%;
      height: 15%;
      margin: 3px;
      padding: 3px;
      overflow: hidden;
    }

    #thumbSVG,
    #mainSVG {
      height: 100%;
      width: 100%;
    }

    #thumbView {
      z-index: 110;
      background-color: white;
    }

    #scopeContainer {
      z-index: 120;
    }
    </style>

    <body>
      <div id="mainViewContainer">
        <div id="mainView">
        </div>
      </div>

      <div id="thumbViewContainer">
        <svg id="scopeContainer" class="thumbViewClass">
            <g>
              <rect id="scope" fill="blue" fill-opacity="0.1" stroke="blue" stroke-width="2px" x="0" y="0" width="0" height="0"/>
              <line id="line1" stroke="blue" stroke-width="2px" x1="0" y1="0" x2="0" y2="0"/>
              <line id="line2" stroke="blue" stroke-width="2px" x1="0" y1="0" x2="0" y2="0"/>
            </g>
          </svg>
        <div id="thumbView" class="thumbViewClass">
        </div>
      </div>

      <!-- Scripts -->
      <script>
        var thumbnailViewer = function(options) {
      var getSVGDocument = function(objectElem) {
        var svgDoc = objectElem.contentDocument;
        if (!svgDoc) {
          if (typeof objectElem.getSVGDocument === "function") {
            svgDoc = objectElem.getSVGDocument();
          }
        }
        return svgDoc;
      }

      var bindThumbnail = function(main, thumb, scopeContainerId) {
        if (!window.main && main) {
          window.main = main;
        }
        if (!window.thumb && thumb) {
          window.thumb = thumb;
        }
        if (!window.main || !window.thumb) {
          return;
        }

        var resizeTimer;
        var interval = 300; 
        window.addEventListener('resize', function(event) {
          if (resizeTimer !== false) {
            clearTimeout(resizeTimer);
          }
          resizeTimer = setTimeout(function() {
            window.main.resize();
            window.thumb.resize();
          }, interval);
        });

        window.main.setOnZoom(function(level) {
          window.thumb.updateThumbScope();
          if (options.onZoom) {
            options.onZoom(window.main, window.thumb, level);
          }
        });

        window.main.setOnPan(function(point) {
          window.thumb.updateThumbScope();
          if (options.onPan) {
            options.onPan(window.main, window.thumb, point);
          }
        });

        var _updateThumbScope = function(main, thumb, scope, line1, line2) {
          var mainPanX = main.getPan().x,
            mainPanY = main.getPan().y,
            mainWidth = main.getSizes().width,
            mainHeight = main.getSizes().height,
            mainZoom = main.getSizes().realZoom,
            thumbPanX = thumb.getPan().x,
            thumbPanY = thumb.getPan().y,
            thumbZoom = thumb.getSizes().realZoom;

          var thumByMainZoomRatio = thumbZoom / mainZoom;

          var scopeX = thumbPanX - mainPanX * thumByMainZoomRatio;
          var scopeY = thumbPanY - mainPanY * thumByMainZoomRatio;
          var scopeWidth = mainWidth * thumByMainZoomRatio;
          var scopeHeight = mainHeight * thumByMainZoomRatio;

          scope.setAttribute("x", scopeX + 1);
          scope.setAttribute("y", scopeY + 1);
          scope.setAttribute("width", scopeWidth - 2);
          scope.setAttribute("height", scopeHeight - 2);
        };

        window.thumb.updateThumbScope = function() {
          var scope = document.getElementById('scope');
          var line1 = document.getElementById('line1');
          var line2 = document.getElementById('line2');
          _updateThumbScope(window.main, window.thumb, scope, line1, line2);
        }
        window.thumb.updateThumbScope();

        var _updateMainViewPan = function(clientX, clientY, scopeContainer, main, thumb) {
          var dim = scopeContainer.getBoundingClientRect(),
            mainWidth = main.getSizes().width,
            mainHeight = main.getSizes().height,
            mainZoom = main.getSizes().realZoom,
            thumbWidth = thumb.getSizes().width,
            thumbHeight = thumb.getSizes().height,
            thumbZoom = thumb.getSizes().realZoom;

          var thumbPanX = clientX - dim.left - thumbWidth / 2;
          var thumbPanY = clientY - dim.top - thumbHeight / 2;
          var mainPanX = -thumbPanX * mainZoom / thumbZoom;
          var mainPanY = -thumbPanY * mainZoom / thumbZoom;
          main.pan({
            x: mainPanX,
            y: mainPanY
          });
        };
        var updateMainViewPan = function(evt, scopeContainerId) {
          if (evt.which == 0 && evt.button == 0) {
            return false;
          }
          var scopeContainer = document.getElementById(scopeContainerId);
          _updateMainViewPan(evt.clientX, evt.clientY, scopeContainer, window.main, window.thumb);
        }

        var scopeContainer = document.getElementById(scopeContainerId);
        scopeContainer.addEventListener('click', function(evt) {
          updateMainViewPan(evt, scopeContainerId);
        });

        scopeContainer.addEventListener('mousemove', function(evt) {
          updateMainViewPan(evt, scopeContainerId);
        });
      };

      var initMainView = function() {
        var mainViewSVGDoc = getSVGDocument(mainViewObjectElem);
        if (options.onMainViewSVGLoaded) {
          options.onMainViewSVGLoaded(mainViewSVGDoc);
        }

        var beforePan = function(oldPan, newPan) {
          var stopHorizontal = false,
            stopVertical = false,
            gutterWidth = 100,
            gutterHeight = 100
            // Computed variables
            ,
            sizes = this.getSizes(),
            leftLimit = -((sizes.viewBox.x + sizes.viewBox.width) * sizes.realZoom) + gutterWidth,
            rightLimit = sizes.width - gutterWidth - (sizes.viewBox.x * sizes.realZoom),
            topLimit = -((sizes.viewBox.y + sizes.viewBox.height) * sizes.realZoom) + gutterHeight,
            bottomLimit = sizes.height - gutterHeight - (sizes.viewBox.y * sizes.realZoom);
          customPan = {};
          customPan.x = Math.max(leftLimit, Math.min(rightLimit, newPan.x));
          customPan.y = Math.max(topLimit, Math.min(bottomLimit, newPan.y));
          return customPan;
        };

        var main = svgPanZoom('#' + options.mainSVGId, {
          zoomEnabled: true,
          controlIconsEnabled: true,
          fit: true,
          center: true,
          beforePan: beforePan,
        });


        bindThumbnail(main, undefined, options.scopeContainerId);
        if (options.onMainViewShown) {
          options.onMainViewShown(mainViewSVGDoc, main);
        }
      };
      var mainViewObjectElem = document.getElementById(options.mainSVGId);
      mainViewObjectElem.addEventListener("load", function() {
        initMainView();
      }, false);

      var initThumbView = function() {
        var thumbViewSVGDoc = getSVGDocument(thumbViewObjectElem);
        if (options.onThumbnailSVGLoaded) {
          options.onThumbnailSVGLoaded(thumbViewSVGDoc);
        }

        var thumb = svgPanZoom('#' + options.thumbSVGId, {
          fit: true,
          zoomEnabled: false,
          panEnabled: false,
          controlIconsEnabled: false,
          dblClickZoomEnabled: false,
          preventMouseEventsDefault: true,
        });

        bindThumbnail(undefined, thumb, options.scopeContainerId);
        if (options.onThumbnailShown) {
          options.onThumbnailShown(thumbViewSVGDoc, thumb);
        }
      };
      var thumbViewObjectElem = document.getElementById(options.thumbSVGId);
      thumbViewObjectElem.addEventListener("load", function() {
        initThumbView();
      }, false);

      initThumbView();
      initMainView();
    };
      </script>

      <script>
        window.onload = function() {
          thumbnailViewer({
            mainSVGId: 'mainSVG',
            thumbSVGId: 'thumbSVG',
            scopeContainerId: 'scopeContainer'
          });
        }
      </script>
    </body>

    </html>
    """
    lines = ''.join(svg_string)
    svg_soup = Soup(lines,features='lxml')
    svg_root_tag_main = svg_soup.find("svg")
    
    svg_root_tag_main.attrs['id'] = 'mainSVG'
    

    soup = Soup(html,features='lxml')
    soup.find(id='mainView').append(svg_root_tag_main)
    soup = Soup(str(soup),features='lxml')
    svg_root_tag_thumb = svg_root_tag_main
    svg_root_tag_thumb.attrs['id'] = 'thumbSVG'
    soup.find(id='thumbView').append(svg_root_tag_thumb)
    soup = Soup(str(soup),features='lxml')
    soup.find('title').append(title_string)
    soup = Soup(str(soup),features='lxml')
    with open(out_file, "w") as file:
        file.write(str(soup))
