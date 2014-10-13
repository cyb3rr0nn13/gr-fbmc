/* -*- c++ -*- */
/* 
 * Copyright 2014 Communications Engineering Lab (CEL), Karlsruhe Institute of Technology (KIT).
 * 
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */


#ifndef INCLUDED_FBMC_COMBINE_IQ_CC_H
#define INCLUDED_FBMC_COMBINE_IQ_CC_H

#include <fbmc/api.h>
#include <gnuradio/sync_decimator.h>

namespace gr {
  namespace fbmc {

    /*!
     * \brief Combines two vectors (first I, then Q) into one vector of complex symbols
     * \ingroup fbmc
     *
     */
    class FBMC_API combine_iq_cc : virtual public gr::sync_decimator
    {
     public:
      typedef boost::shared_ptr<combine_iq_cc> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of fbmc::combine_iq_cc.
       *
       * To avoid accidental use of raw pointers, fbmc::combine_iq_cc's
       * constructor is in a private implementation
       * class. fbmc::combine_iq_cc::make is the public interface for
       * creating new instances.
       */
      static sptr make();
    };

  } // namespace fbmc
} // namespace gr

#endif /* INCLUDED_FBMC_COMBINE_IQ_CC_H */
