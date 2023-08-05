use pyo3::prelude::*;
use pyo3::wrap_pyfunction;


#[pyfunction]
fn fizzbuzz(n: usize) -> Vec<String> {
    let mut l = vec!["".to_string(); n];
    for i in 0..n {
        match (i % 3, i % 5) {
            (0, 0) => l[i] = "FizzBuzz".to_string(),
            (0, _) => l[i] = "Fizz".to_string(),
            (_, 0) => l[i] = "Buzz".to_string(),
            (_, _) => l[i] = i.to_string()
        }
    }
    l
}

#[pymodule]
fn fizzbuzz_rust(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(fizzbuzz, m)?)?;
    Ok(())
}