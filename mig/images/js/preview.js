/*

#
# --- BEGIN_HEADER ---
#
# preview - javascript based image preview library
# Copyright (C) 2003-2015  The MiG Project lead by Brian Vinter
#
# This file is part of MiG.
#
# MiG is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public Licethnse as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# MiG is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
# -- END_HEADER ---
#

*/

/*

This module is based on the CamanJS module: http://camanjs.com/

# Copyright notice follows here:

Copyright (c) 2010, Ryan LeFevre
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, 
are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice, 
      this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright notice, 
      this list of conditions and the following disclaimer in the documentation
      and/or other materials provided with the distribution.
    * Neither the name of Ryan LeFevre nor the names of its contributors may be 
      used to endorse or promote products derived from this software without
      specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND 
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, 
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES 
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; 
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) 
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

*/

Preview = function (selfname, debug) {
	console.debug('Preview: constructor');
    this.selfname = selfname;
    this.image = this.init_image();
    this.histogram = this.init_histogram();
    this.init_min_max_slider(); 
    this.settings = {debug: debug,
                     visible: false,
                     height: 0,
                     zoom: 0,
                     min_zoom: 0,
                     max_zoom: 2
                    };

}

Preview.prototype.get_format_decimals = function() {
    var format_decimals = 4;

    return format_decimals;
}

Preview.prototype.init_preview_struct = function() {

    return {div_id:         null, 
            canvas_id:      null,
            canvas_width:   0,
            canvas_height:  0,
            image_width:    0,
            image_height:   0,
            image_offset_x: 0,
            image_offset_y: 0, 
            image_url:      null,
            image_obj:      new Image()
           };
}

Preview.prototype.init_image = function() {
    var result = this.init_preview_struct();
    result.div_id = "#fm_preview_center_tile";
    result.canvas_id = "#fm_preview_image";

    return result;
}

Preview.prototype.init_histogram = function() {
    var result = this.init_preview_struct();
    result.div_id = "#fm_preview_left_tile_histogram";
    result.canvas_id = "#fm_preview_histogram_image";
    return result;
}

Preview.prototype.clear_canvas = function(canvas) {
    var context = canvas.getContext('2d');

    // Clear rect and ensure white background

    context.clearRect(0, 0, canvas.width, canvas.height);
    context.fillStyle = "#FFFFFF";
    context.fillRect(0, 0, canvas.width, canvas.height);

}

Preview.prototype.set_image_url = function(image_url) {
    this.image.image_url = image_url;
}

Preview.prototype.set_histogram_data = function(data) {
    this.histogram.data = data;
}


Preview.prototype.load_image = function(image_url) {
    this.image_dim_update();
    if (image_url !== undefined) {
        this.image.image_url = image_url;
    }
    this.image_data_load(this.image);
}

Preview.prototype.dim_update = function() {
    this.image_dim_update();
    this.histogram_dim_update();
}

Preview.prototype.image_dim_update = function() {
    var image_border = 1;
    var canvas = $(this.image.canvas_id)[0];
    var context = canvas.getContext('2d');
    var width = $(this.image.div_id).width();
    var height = $(this.image.div_id).height();
    var image_size = width < height ? width : height < width ? height : width;

    context.canvas.width = width;
    context.canvas.height = height;

    image_size -= Math.floor(image_size * (image_border/100.0));

    this.image.canvas_width = width;
    this.image.canvas_height = height;
    this.image.image_width = image_size;
    this.image.image_height = image_size;
    this.image.image_offset_x = Math.floor((width - image_size)/2);
    this.image.image_offset_y = Math.floor((height - image_size)/2);

    console.debug("Preview load image canvas id: " + this.image.div_id);
    console.debug("Preview load image canvas: width: " + width);
    console.debug("Preview load image canvas: height: " + height);
    console.debug("Preview load image_image_size: " + image_size);
    console.debug("Preview load image image_width: " + this.image.image_width);
    console.debug("Preview load image image_height: " + this.image.image_height);
    console.debug("Preview load image x_offset: " + this.image.image_offset_x);
    console.debug("Preview load image y_offset: " + this.image.image_offset_y);
}

Preview.prototype.histogram_dim_update = function() {
    var canvas = $(this.histogram.canvas_id)[0];
    var context = canvas.getContext('2d');
    var width = $(this.histogram.div_id).width();
    var height = width/3;


    console.debug("Preview: update_histogram: width: " + width);
    console.debug("Preview: update_histogram: height: " + height);

    context.canvas.width = width;
    context.canvas.height = height;

    $(this.histogram.div_id).css("height", height);
    this.histogram.image_width = context.canvas.width;
    this.histogram.image_height = context.canvas.height;
    this.histogram.image_offset_x = 0;
    this.histogram.image_offset_y = 0;

    console.debug("Preview load histogram canvas id: " + this.histogram.canvas_id);
    console.debug("Preview load histogram canvas: width: " + width);
    console.debug("Preview load histogram canvas: height: " + height);
    console.debug("Preview load histogram image_width: " + this.histogram.image_width);
    console.debug("Preview load histogram image_height: " + this.histogram.image_height);
    console.debug("Preview load histogram x_offset: " + this.histogram.image_offset_x);
    console.debug("Preview load histogram y_offset: " + this.histogram.image_offset_y);
}

Preview.prototype.load = function(image_url) {
    // If we allready loaded image, then just refresh
    // NOTE: Safari do not trigger onLoad if image_url 
    // is unchanged.
    if (this.image.image_url === image_url) {
        this.refresh();
    }
    else {
        this.load_image(image_url);
        this.draw_histogram();
    }
}


Preview.prototype.refresh = function(callback) {
    if (this.settings.zoom > 0) {
        this.draw_histogram();
        this.image_data_update(this.image, callback);    
    }
}

Preview.prototype.image_data_update = function(preview_struct, callback) {
    var _this = this;
    var canvas = $(preview_struct.canvas_id)[0];
    var context = canvas.getContext('2d');
    
    var min_value = $(this.min_slider_value_id).text();
    var max_value = $(this.max_slider_value_id).text();

    // Update image dimensions

    this.image_dim_update();

    // Caman function calls are put in a queue and
    // when .render() is called

    Caman(preview_struct.canvas_id, function() {

        // Clear rect and ensure white background

        _this.clear_canvas(canvas);
      
        // Draw image

        context.drawImage(preview_struct.image_obj, 
                          preview_struct.image_offset_x,
                          preview_struct.image_offset_y,
                          preview_struct.image_width,
                          preview_struct.image_height);                            

        // Renew Caman canvas from drawn context

        this.replaceCanvas(canvas);

        // Issue a copy of loaded pixel data
        
        this.idmc_reset_original_pixeldata();
        
        // Adjust min/max values

        this.idmc_set_min_max_pixel_values(min_value, max_value);

        // Render image 

        this.render();

        // Callback 

        if (typeof callback === "function") {
            callback();
        }
    });
}

Preview.prototype.image_data_load = function(preview_struct) {
    var preview_obj = this;
    var image_obj = preview_struct.image_obj;
    var image_url = preview_struct.image_url;

    console.debug("Preview: image_data_load -> loading:  " + preview_struct.image_url);
  
    image_obj.onload = function(event) {
      preview_obj.image_data_update(preview_struct);
    };
    image_obj.src = image_url;
}

Preview.prototype.update_preview_min_max_values = function() {
    var max_decimals = this.get_format_decimals();
    var slider_min_value = $("#fm_preview_histogram_min_slider_value").html();
    var slider_max_value = $("#fm_preview_histogram_max_slider_value").html(); 
    var cutoff_min_value = $("#fm_preview_left_output input[name='cutoff_min_value']").val();
    var current_min_value = $("#fm_preview_left_output input[name='current_min_value']").val();
    var current_max_value = $("#fm_preview_left_output input[name='current_max_value']").val();
    var scale_value = $("#fm_preview_left_output input[name='scale_value']").val();

    var new_min_value;
    var new_max_value;

    if (slider_min_value !== undefined &&
        slider_max_value !== undefined &&
        current_min_value !== undefined && 
        current_max_value !== undefined &&
        scale_value !== undefined) {

        slider_min_value = Number(slider_min_value);
        slider_max_value = Number(slider_max_value);
        cutoff_min_value = Number(cutoff_min_value);
        current_min_value = Number(current_min_value);
        current_max_value = Number(current_max_value);
        scale_value = Number(scale_value);
        
        new_min_value = cutoff_min_value + (slider_min_value / scale_value);
        new_max_value = cutoff_min_value + (slider_max_value / scale_value);

        $("#fm_preview_left_output input[name='current_min_value']").val(new_min_value);
        $("#fm_preview_left_output input[name='current_max_value']").val(new_max_value);
        $("#fm_preview_left_output_min_value_show").html("Preview Min: " + Number(new_min_value).toExponential(max_decimals));
        $("#fm_preview_left_output_max_value_show").html("Preview Max: " + Number(new_max_value).toExponential(max_decimals));
        $("#fm_preview_left_output_preview_image_scale_value_show").html("Slider scale: " + Number(scale_value).toExponential(max_decimals));
    }
}

Preview.prototype.init_min_max_slider = function() {
    
    // http://refreshless.com/nouislider/

    var _this = this;

    this.slider_id = "#fm_preview_histogram_min_max_slider";
    this.min_slider_value_id = "#fm_preview_histogram_min_slider_value";
    this.min_slider_value = 0;
    
    this.max_slider_value_id = "#fm_preview_histogram_max_slider_value";
    this.max_slider_value = 255;

    var min_slider_value_id = this.min_slider_value_id;
    var min_slider_value = this.min_slider_value;
    var max_slider_value_id = this.max_slider_value_id;
    var max_slider_value = this.max_slider_value;
    var image = this.image;

    $(this.slider_id).noUiSlider({
        start: [ min_slider_value, max_slider_value ],
        connect: true,
        step: 1,
        range: {
            'min': min_slider_value,
            'max': max_slider_value,
        },    

        // Full number format support.

        format: wNumb({
            mark: ',',
            decimals: 0
        }),
    });
 
    // Setup min slider

    $(this.slider_id).Link('lower').to('-inline-<div class="fm_preview_histogram_min_max_slider_tooltip"></div>', function ( value ) {

        // The tooltip HTML is 'this', so additional markup can be inserted here.

        $(this).html(
            '<br>' +
            '<span id="fm_preview_histogram_min_slider_value">' + value + '</span>'
        );
       
        _this.update_preview_min_max_values();
    });
    
    // Setup max slider

    $(this.slider_id).Link('upper').to('-inline-<div class="fm_preview_histogram_min_max_slider_tooltip"></div>', function ( value ) {

        // The tooltip HTML is 'this', so additional markup can be inserted here.
        $(this).html(
            '<br>' +
            '<span id="fm_preview_histogram_max_slider_value">' + value + '</span>'
            );

        _this.update_preview_min_max_values();
      });
      
      
    // Setup slider change handler

    $(this.slider_id).on('change', function() {    
        var min_value = $(min_slider_value_id).text();
        var max_value = $(max_slider_value_id).text();

        var caman = Caman(image.canvas_id, function() {
            this.idmc_set_min_max_pixel_values(min_value, max_value);
            this.render();
        });
    }); 
}

// Reset sliders 

Preview.prototype.reset = function() {
  var slider_id = this.slider_id;
  var min_slider_value = this.min_slider_value;
  var max_slider_value = this.max_slider_value;
  var image = this.image;

  $(slider_id).val([min_slider_value, max_slider_value]);

  Caman(image.canvas_id, function() {
    this.idmc_set_min_max_pixel_values(min_slider_value, max_slider_value);
    this.render();
  });
}

// Inspired by:
//  http://mihai.sucan.ro/coding/svg-or-canvas/histogram.html

// Check this out:
// https://github.com/devongovett/png.js/blob/master/png.js

Preview.prototype.draw_histogram = function(image_pixel_data) {
    var hist_canvas = $(this.histogram.canvas_id)[0];
    var hist_context = hist_canvas.getContext('2d'); 
    var pixel_bins = this.histogram.data;
    var nr_pixel_bins = pixel_bins.length;

    // Update histogram dimesions

    this.histogram_dim_update();

    // Clear histogram canvas

    this.clear_canvas(hist_canvas);

    // Find maximum

    max_count = Math.max.apply(Math, pixel_bins);
    
    // Draw histogram

    // Define line and fill color

    hist_context.strokeStyle = '#000000';
    hist_context['fillStyle'] = '#000000';

    // Draw border
    
    hist_context.rect(0, 0, hist_canvas.width, hist_canvas.height);
    hist_context.stroke();

    // Draw histogram 

    var border_size = hist_context.lineWidth;
    var max_curve_width = hist_canvas.width;
    var min_curve_x_pos = 0;
    var max_curve_x_pos = hist_canvas.width;

    var max_curve_height = hist_canvas.height - border_size;
    var min_curve_y_pos = hist_canvas.height - border_size;
    var max_curve_y_pos = border_size;

    // Start in lower left corner

    hist_context.beginPath();
    hist_context.moveTo(0, hist_canvas.height);
    
    // Draw curve 

    for (var x, y, i = 0; i < nr_pixel_bins; i++) {
        if (!(i in pixel_bins)) {
          continue;
        }
        y = Math.round((pixel_bins[i]/max_count)*max_curve_height);
        console.debug('i: ' + i + ', x: ' + x + ', y: ' + y + ', pixel_bins[i]: ' + pixel_bins[i] + ', max_count: ' + max_count);
        x = Math.round((i/(nr_pixel_bins-1))*max_curve_width);

        hist_context.lineTo(x, min_curve_y_pos - y);
    }

    // End in lower right corner

    hist_context.lineTo(hist_canvas.width, hist_canvas.height);

    // Draw stroke

    hist_context.stroke();
    
    // Fill curve

    hist_context.fill();
    hist_context.closePath();

    // Update preview min max values

    this.update_preview_min_max_values();
}
