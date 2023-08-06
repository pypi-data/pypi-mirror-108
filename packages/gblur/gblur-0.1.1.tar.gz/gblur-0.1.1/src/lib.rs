mod blur;

use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

#[cfg(test)]
mod test {
    #[test]
    fn test_blur() {
        let mut img = image::open("tests/cballs.png").unwrap();
        let res_img = crate::blur::gblur(&mut img, 1).unwrap();
        let mut f = std::fs::File::create("tests/cballs_blured.png").unwrap();
        res_img.write_to(&mut f, image::ImageFormat::Png).unwrap();
    }
}

/// This is the blur function that can be called from Python. 
/// It takes a slice of bytes and the radius as usize
#[pyfunction]
fn blur(image: &[u8], radius: usize) -> Vec<u8> {
    let mut img = image::load_from_memory(image).unwrap();
    let data = blur::gblur(&mut img, radius).unwrap();
    let mut vec = Vec::new();
    data.write_to(&mut vec, image::ImageFormat::Png).unwrap();
    vec
}

/// Payload function to provide a python module
#[pymodule]
fn gblur(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(blur, m)?)?;
    Ok(())
}
