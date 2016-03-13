#include <iostream>
#include <string>

using namespace std

int main(int argn, char** args)
{
	string str;
	while(getline(cin, str))
	{
		size_t len = str.size();
		for(size_t idx = 0; idx < str.size(); ++idx)
		{
			if(str[idx] == '*' && idx < str.size() - 1 && str[idx+1] == '*')
			{
				//Find end of token
				bool tokenStarted = false;
				size_t lb = 0, rb = 0;
				size_t endIdx = size_t(-1);
				for(size_t i = idx - 1; i >= 0; --i)
				{
					if( !tokenStarted && str[i] == ' ')
						continue;
					if( !tokenStarted )
						tokenStarted = true;
					if( str[i] == ')')
						++rb;
					if( str[i] == '(' )
						++lb;
					if( str[i] == '+' || str[i] == '-' || str[i] == '*' || str[i] == '/' || str[i] == ' ')
					{
						endIdx = i+1;
						break;
					}
				}
				//Find mantise
				size_t mIdx = size_t(-1);
				for(size_t i = idx + 2; i < str.size() && str[i] == ' '; ++i)
					mIdx = i;
				
			}
		}
	}
}
