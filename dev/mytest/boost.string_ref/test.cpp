#include <iostream>
#include <boost/utility/string_ref.hpp>
#include <string>
#include <set>
#include <algorithm>
#include <random>
#include <vector>
#include <functional>

// http://stackoverflow.com/questions/440133/how-do-i-create-a-random-alpha-numeric-string-in-c
typedef std::vector<char> char_array;

char_array charset()
{
    //Change this to suit
    return char_array(
    {'0','1','2','3','4',
    '5','6','7','8','9',
    'A','B','C','D','E','F',
    'G','H','I','J','K',
    'L','M','N','O','P',
    'Q','R','S','T','U',
    'V','W','X','Y','Z',
    'a','b','c','d','e','f',
    'g','h','i','j','k',
    'l','m','n','o','p',
    'q','r','s','t','u',
    'v','w','x','y','z'
    });
};

// given a function that generates a random character,
// return a string of the requested length
std::string random_string( size_t length, std::function<char(void)> rand_char )
{
    std::string str(length,0);
    std::generate_n( str.begin(), length, rand_char );
    return str;
}

int main(int argc, char **argv) {
	if ( 2 != argc ) {
		std::cerr << "invalid number of arguments\n";
		return 1;
	}

	const size_t TOTAL = std::stoull(argv[1]);

	//0) create the character set.
	//   yes, you can use an array here, 
	//   but a function is cleaner and more flexible
	const auto ch_set = charset();

	//1) create a non-deterministic random number generator      
	std::default_random_engine rng(std::random_device{}());

	//2) create a random number "shaper" that will give
	//   us uniformly distributed indices into the character set
	std::uniform_int_distribution<> character_dist(0, ch_set.size()-1);

	//3) create a function that ties them together, to get:
	//   a non-deterministic uniform distribution from the 
	//   character set of your choice.
	auto randchar = [ ch_set,&character_dist,&rng ](){return ch_set[ character_dist(rng) ];};

	std::uniform_int_distribution<> size_dist(5,10);


	std::set<std::string> strings;
	std::set<boost::string_ref> refs;
	for ( size_t n = 0; n < TOTAL; ++n ) {
		auto at = strings.insert(random_string(size_dist(rng), randchar));
		if ( at.second ) {
			auto ref_at = refs.insert(boost::string_ref{*at.first});
			if ( false == ref_at.second ) {
				std::cout.flush();
				std::cerr << "!! " << *at.first << '\n';
			} else {
				std::cout << *at.first << '\n';
			}
		} else {
			std::cout << "! " << *at.first << '\n';
		}
	}

	std::cout << "...\n" << std::flush;
	bool e = (strings.size() == refs.size());
	if ( e ) {
		e = std::equal(strings.begin(), strings.end(), refs.begin());
	}
	if ( e ) {
		std::cout << "equal\n";
	} else {
		std::cout << " ! not equal\n";
	}

	return !e;
}

