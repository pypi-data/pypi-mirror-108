use pyo3::prelude::*;
use pyo3::wrap_pyfunction;


#[pyfunction]
fn fizzbuzz(n: usize) -> Vec<String> {
    let mut l = vec!["".to_string(); n];
    for i in 1..n+1 {
        match (i % 3, i % 5) {
            (0, 0) => l[i-1] = "FizzBuzz".to_string(),
            (0, _) => l[i-1] = "Fizz".to_string(),
            (_, 0) => l[i-1] = "Buzz".to_string(),
            (_, _) => l[i-1] = i.to_string()
        }
    }
    l
}

#[pymodule]
fn fizzbuzz_rust(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(fizzbuzz, m)?)?;
    Ok(())
}