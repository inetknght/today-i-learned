// g++ test.cpp -std=c++11 -l boost_system -l boost_iostreams
// ./a.out

#include <iostream>
#include <boost/iostreams/device/mapped_file.hpp>
#include <cstdint>

namespace bio = boost::iostreams;
int main(int argc, char **argv) {

	bio::mapped_file_source file;

	{
		bio::mapped_file_source file2;
		try {
			file2.open(argv[0]);
		} catch ( const std::ios::failure & e) {
			std::cerr << e.what() << '\n';
			return 1;
		}
		file = std::move(file2);
		std::cout << (void*)file.data() << '\t' << (void*)file2.data() << '\n';
		file2.close();
	}

	// if == 0, then closing file2 closed file.
	// if commenting out file2.close() above and this becomes nonzero, then iostream is copied and not moved.
	std::cout << (void*)file.data() << '\n';

// compiler error: bio::mapped_file_source does not inerhit from std::istream
//	std::string line;
//	while ( std::getline(file, line) ) {
//		std::cout << "gotline\n";
//	}

	return 0;
}

