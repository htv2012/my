.PHONY: \
	all \
	bench \
	build \
	clean \
	format \
	lint \
	run \
	test \


### One dev cycle
all: run

### Build release version
build:
	cargo build --release

### Static analysis
lint:
	cargo clippy

### Format code
format:
	cargo fmt

### Run all tests
test:
	cargo test

### Runsthe cli
run: lint format build test
	cargo run --

### Perform benchmark
bench:
	cargo bench
	open target/criterion/report/index.html

### Delete generated files
clean:
	cargo clean

