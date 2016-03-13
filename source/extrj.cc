#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <cmath>
#include <cassert>
#include <cstdlib>

using namespace std;

const string D = ";";

int main(int argn, char** args)
{
	if ( argn < 3 || argn > 4 )
	{
		cout << " usage : " << args[0] << " <input d.file> <output common name> <point_type>" << endl;
		return -1;
	}
	
	string ifname = args[1];
	string ofmask = args[2];
	
	int pointType = 0;
	if ( argn == 4 )
		pointType = atoi( args[3] );

	size_t ibr; //   :	  the index of the branch
	size_t ntot; //  :	  the index of the point
	int itp; //   :	  the type of point
	size_t lab; //   :	  the label of the point
	size_t nfpr; //  :	  the number of free parameters used in the computation
	size_t isw; //   :	  the value of isw used in the computation
	size_t ntpl; //  :	  the number of points in the time interval [0,1]
		         // for which solution data are written
	size_t nar; //   :	  the number of values written per point
		        //  (nar=ndim+1, since t and u(i), i=1,..,ndim are written)
	size_t nrowpr; //:	  the number of lines printed following the identifying line
		          //and before the next data set or the end of the file
		          //(used for quickly skipping a data set when searching)
	size_t ntst; //  :	  the number of time intervals used in the discretization
	size_t ncol;  //:	  the number of collocation points used
	size_t nparx; // :	  the dimension of the array par
	
	double skip;
	
	// input file
	ifstream fin(ifname.c_str());
	// output file
	size_t f_idx = 0;
	ofstream fout;

	while(!fin.eof())
	{
		//reading first parameters line
		bool good_spec = ( fin >> ibr >> ntot >> itp >> lab >> nfpr >> isw >> ntpl >> nar >> nrowpr >> ntst >> ncol >> nparx
			>> skip >> skip >> skip >> skip );
		//if can't read first line - exit	
		if (!good_spec)
		{
			fout.close();
			return 0;
		}

		//open file for write coordinates
		if( itp == pointType )
		{
			char osnum[256];
			sprintf(osnum, "%02d", f_idx++ );
			string ofname = ofmask + "_pt_" + string(osnum);
			fout.open(ofname.c_str());
			if ( !fout.good() )
			{
				cout << " error : can't open file " << ofname << " for writing" << endl;
				return -1;
			}		
		}
		//read coordinates from fort.8 or s.*** file
		for( size_t p_idx = 0; p_idx < ntpl; ++p_idx)
		{
			for( size_t idx = 0; idx < nar; ++idx )
			{
				double value;
				fin >> value;
				if(itp == pointType)
				{
					fout << value;
					if( idx < nar - 1 )
						fout << ';';
					else
						fout << endl;
				}
			}
		}
		if(itp == pointType)
			fout.close();
		//skip icps
		for (size_t idx = 0; idx < nfpr; ++idx)
			fin >> skip;
		//skip parameters derivatives
		for (size_t idx = 0; idx < nfpr; ++idx)
			fin >> skip;
		//skip coords derivatives
		for (size_t idx = 0; idx < ntpl; ++idx)
			for(size_t iidx = 0; iidx < nar - 1; ++iidx)
				fin >> skip;
		//skip parameters
		for(size_t idx = 0; idx < nparx; ++idx)
			fin >> skip;
			
	}
	return 0;
}

/*
first identifying line:

      ibr   :	  the index of the branch
      ntot  :	  the index of the point
      itp   :	  the type of point
      lab   :	  the label of the point
      nfpr  :	  the number of free parameters used in the computation
      isw   :	  the value of isw used in the computation
      ntpl  :	  the number of points in the time interval [0,1]
		          for which solution data are written
      nar   :	  the number of values written per point
		          (nar=ndim+1, since t and u(i), i=1,..,ndim are written)
      nrowpr:	  the number of lines printed following the identifying line
		          and before the next data set or the end of the file
		          (used for quickly skipping a data set when searching)
      ntst  :	  the number of time intervals used in the discretization
      ncol  :	  the number of collocation points used
      nparx :	  the dimension of the array par

following this are ntpl lines containing
      t u_1(t) u_2(t) ... u_ndim(t)

following this is a line containing the indices of the free parameters
      icp(i) for i=1,...,nfpr

followed by a line containing the derivative of parameters wrt arclength
      rl_dot(i) for i=1,...,nfpr

following this are ntpl lines containing the derivative of the solution wrt arclength
      u_dot_1(t) u_dot_2(t) ... u_dot_ndim(t)

followed by the parameter values 
      par(i) for i=1,...,nparx
*/
