use image::{DynamicImage, RgbImage, RgbaImage};

/// gblur matches the DynamicImage enum and calls int_blur with specific parameters.
pub fn gblur(image: &mut DynamicImage, radius: usize) -> Option<DynamicImage> {
    match image {
        DynamicImage::ImageRgb8(i) => Some(int3_blur(i.as_raw(), i.width(), i.height(), 3, radius)),
        DynamicImage::ImageRgba8(i) => {
            Some(int4_blur(i.as_raw(), i.width(), i.height(), 4, radius))
        }
        _ => None,
    }
}

/// int_blur3 is the internal blur function for 3 channel images.
/// It takes multiple parameters:
/// - raw as a slice of u8, the raw bytes
/// - width - the width of the image
/// - heigth - the height of the image
/// - channels - the number of channels
/// - radius - the radius for the blurring
/// It returns a dynamic image which can be used to display the content of the file.
fn int3_blur(raw: &[u8], width: u32, height: u32, channels: u32, radius: usize) -> DynamicImage {
    let width = width as usize;
    let height = height as usize;
    let channels = channels as usize;
    let size = width * height;
    let mut red_data = vec![0; size];
    let mut green_data = vec![0; size];
    let mut blue_data = vec![0; size];
    let mut counter = 0;
    // Copy raw bytes in the specific data entries
    for i in (0..size * channels).step_by(channels) {
        red_data[counter] = raw[i];
        green_data[counter] = raw[i + 1];
        blue_data[counter] = raw[i + 2];
        counter += 1;
    }
    // Applies gaussian blurs to all channels
    rayon::scope(|s| {
        s.spawn(|_| gaussian_blur(&mut red_data, width, height, radius));
        s.spawn(|_| gaussian_blur(&mut green_data, width, height, radius));
        s.spawn(|_| gaussian_blur(&mut blue_data, width, height, radius));
    });
    let mut raw = vec![0u8; size * channels];
    counter = 0;
    // Copy bytes from the data buffer back to the array
    for i in (0..size * channels).step_by(channels) {
        raw[i] = red_data[counter];
        raw[i + 1] = green_data[counter];
        raw[i + 2] = blue_data[counter];
        counter += 1;
    }
    // Converts the byte array to an image
    match RgbImage::from_vec(width as u32, height as u32, raw) {
        Some(it) => DynamicImage::ImageRgb8(it),
        None => unreachable!(),
    }
}

/// int_blur4 is the internal blur function for 3 channel images.
/// It takes multiple parameters:
/// - raw as a slice of u8, the raw bytes
/// - width - the width of the image
/// - heigth - the height of the image
/// - channels - the number of channels
/// - radius - the radius for the blurring
/// It returns a dynamic image which can be used to display the content of the file.
fn int4_blur(raw: &[u8], width: u32, height: u32, channels: u32, radius: usize) -> DynamicImage {
    let width = width as usize;
    let height = height as usize;
    let channels = channels as usize;
    let size = width * height;
    let mut red_data = vec![0; size];
    let mut green_data = vec![0; size];
    let mut blue_data = vec![0; size];
    let mut alpha_data = vec![0; size];
    let mut counter = 0;
    // Copy raw bytes in the specific data entries
    for i in (0..size * channels).step_by(channels) {
        red_data[counter] = raw[i];
        green_data[counter] = raw[i + 1];
        blue_data[counter] = raw[i + 2];
        alpha_data[counter] = raw[i + 3];
        counter += 1;
    }
    // Applies gaussian blurs to all channels
    rayon::scope(|s| {
        s.spawn(|_| gaussian_blur(&mut red_data, width, height, radius));
        s.spawn(|_| gaussian_blur(&mut green_data, width, height, radius));
        s.spawn(|_| gaussian_blur(&mut blue_data, width, height, radius));
        s.spawn(|_| gaussian_blur(&mut alpha_data, width, height, radius));
    });
    let mut raw = vec![0u8; size * channels];
    counter = 0;
    // Copy bytes from the data buffer back to the array
    for i in (0..size * channels).step_by(channels) {
        raw[i] = red_data[counter];
        raw[i + 1] = green_data[counter];
        raw[i + 2] = blue_data[counter];
        raw[i + 3] = alpha_data[counter];
        counter += 1;
    }
    match RgbaImage::from_vec(width as u32, height as u32, raw) {
        Some(it) => DynamicImage::ImageRgba8(it),
        _ => unreachable!(),
    }
}

/// Applies gaussian blur on the scl buffer
// implementation of http://blog.ivank.net/fastest-gaussian-blur.html
fn gaussian_blur(scl: &mut Vec<u8>, width: usize, height: usize, radius: usize) {
    let boxes = boxes_for_gauss(radius as isize, 3);
    let mut tcl = vec![0u8; width * height];
    box_blur_full(scl, &mut tcl, width, height, (boxes[0] - 1) / 2);
    box_blur_full(&mut tcl, scl, width, height, (boxes[1] - 1) / 2);
    box_blur_full(scl, &mut tcl, width, height, (boxes[2] - 1) / 2);
}

/// Generates the boxes for the gaussian blur
fn boxes_for_gauss(sigma: isize, n: isize) -> Vec<usize> {
    let avg = f64::sqrt((12 * sigma * sigma) as f64 / n as f64 + 1f64);
    let mut wfloor = f64::floor(avg) as isize;
    if wfloor % 2 == 0 {
        wfloor -= 1;
    }
    let wu = wfloor + 2;
    let a = 12 * sigma * sigma - n * wfloor * wfloor - 4 * n * wfloor - 3 * n;
    let b = -4 * wfloor - 4;
    let med_ideal = a as f64 / b as f64;
    let med_round = f64::round(med_ideal) as usize;
    let mut v = vec![0; n as usize];
    for i in 0..n as usize {
        if i < med_round {
            v[i] = wfloor as usize;
        } else {
            v[i] = wu as usize;
        }
    }
    v
}

fn box_blur_full(scl: &mut Vec<u8>, tcl: &mut Vec<u8>, width: usize, height: usize, radius: usize) {
    for i in 0..width * height {
        tcl[i] = scl[i];
    }
    box_blur_horizontal(tcl, scl, width, height, radius);
    box_blur_total(scl, tcl, width, height, radius);
}

fn box_blur_horizontal(
    scl: &mut Vec<u8>,
    tcl: &mut Vec<u8>,
    width: usize,
    height: usize,
    radius: usize,
) {
    let iarr = 1f64 / (radius + radius + 1) as f64;
    for i in 0..height {
        let mut ti = i * width;
        let mut li = ti;
        let mut ri = ti + radius;
        let fval = scl[ti] as usize;
        let lval = scl[ti + width - 1] as usize;
        let mut val = ((radius + 1) * fval) as i32;
        for j in 0..radius {
            val += scl[ti + j as usize] as i32;
        }
        for _j in 0..radius + 1 {
            val += scl[ri] as i32 - fval as i32;
            tcl[ti] = f64::round(val as f64 * iarr) as u8;
            ri += 1;
            ti += 1;
        }
        for _j in radius + 1..width - radius {
            val += scl[ri] as i32 - scl[li] as i32;
            tcl[ti] = f64::round(val as f64 * iarr) as u8;
            ri += 1;
            li += 1;
            ti += 1;
        }
        for _j in width - radius..width {
            val += lval as i32 - scl[li] as i32;
            tcl[ti] = f64::round(val as f64 * iarr) as u8;
            li += 1;
            ti += 1;
        }
    }
}

fn box_blur_total(
    scl: &mut Vec<u8>,
    tcl: &mut Vec<u8>,
    width: usize,
    height: usize,
    radius: usize,
) {
    let iarr = 1f64 / (radius + radius + 1) as f64;
    for i in 0..width {
        let mut ti = i;
        let mut li = ti;
        let mut ri = ti + radius * width;
        let fval = scl[ti] as usize;
        let lval = scl[ti + width * (height - 1)] as usize;
        let mut val = ((radius + 1) * fval) as i32;
        for j in 0..radius {
            val += scl[ti + j as usize * width] as i32;
        }
        for _j in 0..radius + 1 {
            val += scl[ri] as i32 - fval as i32;
            tcl[ti] = f64::round(val as f64 * iarr) as u8;
            ri += width;
            ti += width;
        }
        for _j in radius + 1..height - radius {
            val += scl[ri] as i32 - scl[li] as i32;
            tcl[ti] = f64::round(val as f64 * iarr) as u8;
            ri += width;
            li += width;
            ti += width;
        }
        for _j in height - radius..height {
            val += lval as i32 - scl[li] as i32;
            tcl[ti] = f64::round(val as f64 * iarr) as u8;
            li += width;
            ti += width;
        }
    }
}
