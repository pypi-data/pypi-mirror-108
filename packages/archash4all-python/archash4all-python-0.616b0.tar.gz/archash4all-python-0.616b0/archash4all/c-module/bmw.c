/* Blue Midnight Wish hash function as it will be submitted to
   NIST for the second round of SHA-3 competition.
   Changes in this version (compared to the version submitted for the Round 1):
   1. Corrected IV for 224 and 384 version.
   2. Tweaked f0() and f1()
   3. Use of final compression function invocation.
*/

/* This is a reference C code for Blue Midnight Wish hash function
   as it will be submitted to NIST for the second round of SHA-3 competition.
   Programmed by Danilo Gligoroski, August 2009.
*/

#include "bmw.h"
#include <string.h>

/* BlueMidnightWish384 initial double chaining pipe */
const u_int64_t i384p2[16] =
{
  0x0001020304050607ull, 0x08090a0b0c0d0e0full,
  0x1011121314151617ull, 0x18191a1b1c1d1e1full,
  0x2021222324252627ull, 0x28292a2b2c2d2e2full,
  0x3031323334353637ull, 0x38393a3b3c3d3e3full,
  0x4041424344454647ull, 0x48494a4b4c4d4e4full,
  0x5051525354555657ull, 0x58595a5b5c5d5e5full,
  0x6061626364656667ull, 0x68696a6b6c6d6e6full,
  0x7071727374757677ull, 0x78797a7b7c7d7e7full
};

#define LROTL32(x, n) (((x) << (n)) | ((x) >> (32 - (n))))
#define ROTR32(x, n) (((x) >> (n)) | ((x) << (32 - (n))))

#define ROTL64(x, n) (((x) << (n)) | ((x) >> (64 - (n))))
#define ROTR64(x, n) (((x) >> (n)) | ((x) << (64 - (n))))

#define SHL(x, n) ((x) << n)
#define SHR(x, n) ((x) >> n)

/* Components used for 384 and 512 bit version */
#define s64_0(x) (SHR((x), 1) ^ SHL((x), 3) ^ ROTL64((x), 4) ^ ROTL64((x), 37))
#define s64_1(x) (SHR((x), 1) ^ SHL((x), 2) ^ ROTL64((x), 13) ^ ROTL64((x), 43))
#define s64_2(x) (SHR((x), 2) ^ SHL((x), 1) ^ ROTL64((x), 19) ^ ROTL64((x), 53))
#define s64_3(x) (SHR((x), 2) ^ SHL((x), 2) ^ ROTL64((x), 28) ^ ROTL64((x), 59))
#define s64_4(x) (SHR((x), 1) ^ (x))
#define s64_5(x) (SHR((x), 2) ^ (x))
#define r64_01(x) ROTL64((x), 5)
#define r64_02(x) ROTL64((x), 11)
#define r64_03(x) ROTL64((x), 27)
#define r64_04(x) ROTL64((x), 32)
#define r64_05(x) ROTL64((x), 37)
#define r64_06(x) ROTL64((x), 43)
#define r64_07(x) ROTL64((x), 53)

#define hashState384(x) ((x)->pipe->p512)

static Data512 *hashState512(HashState *h)
{
  return h->pipe->p512;
}

/* Message expansion function 1 */
static u_int64_t expand64_1(int i, u_int64_t *M64, u_int64_t *H, u_int64_t *Q)
{
  return (s64_1(Q[i - 16]) + s64_2(Q[i - 15]) + s64_3(Q[i - 14]) + s64_0(Q[i - 13]) + s64_1(Q[i - 12]) + s64_2(Q[i - 11]) + s64_3(Q[i - 10]) + s64_0(Q[i - 9]) + s64_1(Q[i - 8]) + s64_2(Q[i - 7]) + s64_3(Q[i - 6]) + s64_0(Q[i - 5]) + s64_1(Q[i - 4]) + s64_2(Q[i - 3]) + s64_3(Q[i - 2]) + s64_0(Q[i - 1]) + ((i * (0x0555555555555555ull) + ROTL64(M64[(i - 16) % 16], ((i - 16) % 16) + 1) + ROTL64(M64[(i - 13) % 16], ((i - 13) % 16) + 1) - ROTL64(M64[(i - 6) % 16], ((i - 6) % 16) + 1)) ^ H[(i - 16 + 7) % 16]));
}

/* Message expansion function 2 */
static u_int64_t expand64_2(int i, u_int64_t *M64, u_int64_t *H, u_int64_t *Q)
{
  return (Q[i - 16] + r64_01(Q[i - 15]) + Q[i - 14] + r64_02(Q[i - 13]) + Q[i - 12] + r64_03(Q[i - 11]) + Q[i - 10] + r64_04(Q[i - 9]) + Q[i - 8] + r64_05(Q[i - 7]) + Q[i - 6] + r64_06(Q[i - 5]) + Q[i - 4] + r64_07(Q[i - 3]) + s64_4(Q[i - 2]) + s64_5(Q[i - 1]) + ((i * (0x0555555555555555ull) + ROTL64(M64[(i - 16) % 16], ((i - 16) % 16) + 1) + ROTL64(M64[(i - 13) % 16], ((i - 13) % 16) + 1) - ROTL64(M64[(i - 6) % 16], ((i - 6) % 16) + 1)) ^ H[(i - 16 + 7) % 16]));
}

static void Compression512(u_int64_t *M64, u_int64_t *H)
{
  int i;
  u_int64_t XL64, XH64, W[32], Q[32];

  /*  This part is the function f0 - in the documentation */

  /*  First we mix the message block *M64 (M in the documatation)        */
  /*  with the previous double pipe *P.                                  */
  /*  For a fixed previous double pipe, or fixed message block, this     */
  /*  part is bijection.                                                 */
  /*  This transformation diffuses every one bit difference in 5 words.  */
  W[0] = (M64[5] ^ H[5]) - (M64[7] ^ H[7]) + (M64[10] ^ H[10]) + (M64[13] ^ H[13]) + (M64[14] ^ H[14]);
  W[1] = (M64[6] ^ H[6]) - (M64[8] ^ H[8]) + (M64[11] ^ H[11]) + (M64[14] ^ H[14]) - (M64[15] ^ H[15]);
  W[2] = (M64[0] ^ H[0]) + (M64[7] ^ H[7]) + (M64[9] ^ H[9]) - (M64[12] ^ H[12]) + (M64[15] ^ H[15]);
  W[3] = (M64[0] ^ H[0]) - (M64[1] ^ H[1]) + (M64[8] ^ H[8]) - (M64[10] ^ H[10]) + (M64[13] ^ H[13]);
  W[4] = (M64[1] ^ H[1]) + (M64[2] ^ H[2]) + (M64[9] ^ H[9]) - (M64[11] ^ H[11]) - (M64[14] ^ H[14]);
  W[5] = (M64[3] ^ H[3]) - (M64[2] ^ H[2]) + (M64[10] ^ H[10]) - (M64[12] ^ H[12]) + (M64[15] ^ H[15]);
  W[6] = (M64[4] ^ H[4]) - (M64[0] ^ H[0]) - (M64[3] ^ H[3]) - (M64[11] ^ H[11]) + (M64[13] ^ H[13]);
  W[7] = (M64[1] ^ H[1]) - (M64[4] ^ H[4]) - (M64[5] ^ H[5]) - (M64[12] ^ H[12]) - (M64[14] ^ H[14]);
  W[8] = (M64[2] ^ H[2]) - (M64[5] ^ H[5]) - (M64[6] ^ H[6]) + (M64[13] ^ H[13]) - (M64[15] ^ H[15]);
  W[9] = (M64[0] ^ H[0]) - (M64[3] ^ H[3]) + (M64[6] ^ H[6]) - (M64[7] ^ H[7]) + (M64[14] ^ H[14]);
  W[10] = (M64[8] ^ H[8]) - (M64[1] ^ H[1]) - (M64[4] ^ H[4]) - (M64[7] ^ H[7]) + (M64[15] ^ H[15]);
  W[11] = (M64[8] ^ H[8]) - (M64[0] ^ H[0]) - (M64[2] ^ H[2]) - (M64[5] ^ H[5]) + (M64[9] ^ H[9]);
  W[12] = (M64[1] ^ H[1]) + (M64[3] ^ H[3]) - (M64[6] ^ H[6]) - (M64[9] ^ H[9]) + (M64[10] ^ H[10]);
  W[13] = (M64[2] ^ H[2]) + (M64[4] ^ H[4]) + (M64[7] ^ H[7]) + (M64[10] ^ H[10]) + (M64[11] ^ H[11]);
  W[14] = (M64[3] ^ H[3]) - (M64[5] ^ H[5]) + (M64[8] ^ H[8]) - (M64[11] ^ H[11]) - (M64[12] ^ H[12]);
  W[15] = (M64[12] ^ H[12]) - (M64[4] ^ H[4]) - (M64[6] ^ H[6]) - (M64[9] ^ H[9]) + (M64[13] ^ H[13]);

  /*  Diffuse the differences in every word in a bijective manner with s64_i, and then add the values of the previous double pipe.*/
  Q[0] = s64_0(W[0]) + H[1];
  Q[1] = s64_1(W[1]) + H[2];
  Q[2] = s64_2(W[2]) + H[3];
  Q[3] = s64_3(W[3]) + H[4];
  Q[4] = s64_4(W[4]) + H[5];
  Q[5] = s64_0(W[5]) + H[6];
  Q[6] = s64_1(W[6]) + H[7];
  Q[7] = s64_2(W[7]) + H[8];
  Q[8] = s64_3(W[8]) + H[9];
  Q[9] = s64_4(W[9]) + H[10];
  Q[10] = s64_0(W[10]) + H[11];
  Q[11] = s64_1(W[11]) + H[12];
  Q[12] = s64_2(W[12]) + H[13];
  Q[13] = s64_3(W[13]) + H[14];
  Q[14] = s64_4(W[14]) + H[15];
  Q[15] = s64_0(W[15]) + H[0];

  /* This is the Message expansion or f_1 in the documentation.       */
  /* It has 16 rounds.                                                */
  /* Blue Midnight Wish has two tunable security parameters.          */
  /* The parameters are named EXPAND_1_ROUNDS and EXPAND_2_ROUNDS.    */
  /* The following relation for these parameters should is satisfied: */
  /* EXPAND_1_ROUNDS + EXPAND_2_ROUNDS = 16                           */

  for (i = 0; i < EXPAND_1_ROUNDS; i++)
    Q[i + 16] = expand64_1(i + 16, M64, H, Q);
  for (i = EXPAND_1_ROUNDS; i < EXPAND_1_ROUNDS + EXPAND_2_ROUNDS; i++)
    Q[i + 16] = expand64_2(i + 16, M64, H, Q);

  /* Blue Midnight Wish has two temporary cummulative variables that accumulate via XORing */
  /* 16 new variables that are prooduced in the Message Expansion part.                    */
  XL64 = Q[16] ^ Q[17] ^ Q[18] ^ Q[19] ^ Q[20] ^ Q[21] ^ Q[22] ^ Q[23];
  XH64 = XL64 ^ Q[24] ^ Q[25] ^ Q[26] ^ Q[27] ^ Q[28] ^ Q[29] ^ Q[30] ^ Q[31];

  /*  This part is the function f_2 - in the documentation            */

  /*  Compute the double chaining pipe for the next message block.    */
  H[0] = (SHL(XH64, 5) ^ SHR(Q[16], 5) ^ M64[0]) + (XL64 ^ Q[24] ^ Q[0]);
  H[1] = (SHR(XH64, 7) ^ SHL(Q[17], 8) ^ M64[1]) + (XL64 ^ Q[25] ^ Q[1]);
  H[2] = (SHR(XH64, 5) ^ SHL(Q[18], 5) ^ M64[2]) + (XL64 ^ Q[26] ^ Q[2]);
  H[3] = (SHR(XH64, 1) ^ SHL(Q[19], 5) ^ M64[3]) + (XL64 ^ Q[27] ^ Q[3]);
  H[4] = (SHR(XH64, 3) ^ Q[20] ^ M64[4]) + (XL64 ^ Q[28] ^ Q[4]);
  H[5] = (SHL(XH64, 6) ^ SHR(Q[21], 6) ^ M64[5]) + (XL64 ^ Q[29] ^ Q[5]);
  H[6] = (SHR(XH64, 4) ^ SHL(Q[22], 6) ^ M64[6]) + (XL64 ^ Q[30] ^ Q[6]);
  H[7] = (SHR(XH64, 11) ^ SHL(Q[23], 2) ^ M64[7]) + (XL64 ^ Q[31] ^ Q[7]);

  H[8] = ROTL64(H[4], 9) + (XH64 ^ Q[24] ^ M64[8]) + (SHL(XL64, 8) ^ Q[23] ^ Q[8]);
  H[9] = ROTL64(H[5], 10) + (XH64 ^ Q[25] ^ M64[9]) + (SHR(XL64, 6) ^ Q[16] ^ Q[9]);
  H[10] = ROTL64(H[6], 11) + (XH64 ^ Q[26] ^ M64[10]) + (SHL(XL64, 6) ^ Q[17] ^ Q[10]);
  H[11] = ROTL64(H[7], 12) + (XH64 ^ Q[27] ^ M64[11]) + (SHL(XL64, 4) ^ Q[18] ^ Q[11]);
  H[12] = ROTL64(H[0], 13) + (XH64 ^ Q[28] ^ M64[12]) + (SHR(XL64, 3) ^ Q[19] ^ Q[12]);
  H[13] = ROTL64(H[1], 14) + (XH64 ^ Q[29] ^ M64[13]) + (SHR(XL64, 4) ^ Q[20] ^ Q[13]);
  H[14] = ROTL64(H[2], 15) + (XH64 ^ Q[30] ^ M64[14]) + (SHR(XL64, 7) ^ Q[21] ^ Q[14]);
  H[15] = ROTL64(H[3], 16) + (XH64 ^ Q[31] ^ M64[15]) + (SHR(XL64, 2) ^ Q[22] ^ Q[15]);
}

HashReturn Init(HashState *state, int hashbitlen)
{
  state->hashbitlen = 384;
  // #1 Between comments #1 and #2 add algorithm specific initialization
  state->bits_processed = 0;
  state->unprocessed_bits = 0;
  memcpy(hashState384(state)->DoublePipe, i384p2, 16 * sizeof(u_int64_t));
  // #2 Between comments #1 and #2 add algorithm specific initialization
  return (SUCCESS);
}

HashReturn Update(HashState *state, const BitSequence *data, DataLength databitlen)
{
  u_int32_t *M32, *H256;
  u_int64_t *M64, *H512;
  int LastBytes;

  if (state->unprocessed_bits > 0)
  {
    if (state->unprocessed_bits + databitlen > H1_512_BLOCK_SIZE * 8)
    {
      return BAD_CONSECUTIVE_CALL_TO_UPDATE;
    }
    else
    {
      LastBytes = (int)databitlen >> 3; // LastBytes = databitlen / 8
      memcpy(hashState512(state)->LastPart + (state->unprocessed_bits >> 3), data, LastBytes);
      state->unprocessed_bits += (int)databitlen;
      databitlen = state->unprocessed_bits;
      M64 = (u_int64_t *)hashState512(state)->LastPart;
    }
  }
  else
    M64 = (u_int64_t *)data;

  H512 = hashState512(state)->DoublePipe;
  while (databitlen >= H1_512_BLOCK_SIZE * 8)
  {
    databitlen -= H1_512_BLOCK_SIZE * 8;
    // #1 Between comments #1 and #2 add algorithm specifics

    state->bits_processed += H1_512_BLOCK_SIZE * 8;
    Compression512(M64, H512);
    M64 += 16;
  }
  state->unprocessed_bits = (int)databitlen;
  if (databitlen > 0)
  {
    LastBytes = ((~(((-(int)databitlen) >> 3) & 0x03ff)) + 1) & 0x03ff; // LastBytes = Ceil(databitlen / 8)
    memcpy(hashState512(state)->LastPart, M64, LastBytes);
  }
  // #2 Between comments #1 and #2 add algorithm specifics
  return (SUCCESS);
}

HashReturn Final(HashState *state, BitSequence *hashval)
{
  u_int32_t *M32, *H256;
  u_int64_t *M64, *H512;
  DataLength databitlen;
  int LastByte, PadOnePosition;

  u_int32_t CONST32final[16] =
  {
    0xaaaaaaa0ul, 0xaaaaaaa1ul, 0xaaaaaaa2ul, 0xaaaaaaa3ul,
    0xaaaaaaa4ul, 0xaaaaaaa5ul, 0xaaaaaaa6ul, 0xaaaaaaa7ul,
    0xaaaaaaa8ul, 0xaaaaaaa9ul, 0xaaaaaaaaul, 0xaaaaaaabul,
    0xaaaaaaacul, 0xaaaaaaadul, 0xaaaaaaaeul, 0xaaaaaaaful
  };

  u_int64_t CONST64final[16] =
  {
    0xaaaaaaaaaaaaaaa0ull, 0xaaaaaaaaaaaaaaa1ull,
    0xaaaaaaaaaaaaaaa2ull, 0xaaaaaaaaaaaaaaa3ull,
    0xaaaaaaaaaaaaaaa4ull, 0xaaaaaaaaaaaaaaa5ull,
    0xaaaaaaaaaaaaaaa6ull, 0xaaaaaaaaaaaaaaa7ull,
    0xaaaaaaaaaaaaaaa8ull, 0xaaaaaaaaaaaaaaa9ull,
    0xaaaaaaaaaaaaaaaaull, 0xaaaaaaaaaaaaaaabull,
    0xaaaaaaaaaaaaaaacull, 0xaaaaaaaaaaaaaaadull,
    0xaaaaaaaaaaaaaaaeull, 0xaaaaaaaaaaaaaaafull
  };

  H256 = NULL, H512 = NULL;

  LastByte = (int)state->unprocessed_bits >> 3;
  PadOnePosition = 7 - (state->unprocessed_bits & 0x07);

  hashState512(state)->LastPart[LastByte] = (hashState512(state)->LastPart[LastByte]
    & (0xff << (PadOnePosition + 1))) ^ (0x01 << PadOnePosition);

  M64 = (u_int64_t *)hashState512(state)->LastPart;

  if (state->unprocessed_bits < 960)
  {
    memset((hashState512(state)->LastPart) + LastByte + 1, 0x00, H1_512_BLOCK_SIZE - LastByte - 9);
    databitlen = H1_512_BLOCK_SIZE * 8;
    M64[15] = state->bits_processed + state->unprocessed_bits;
  }
  else
  {
    memset((hashState512(state)->LastPart) + LastByte + 1, 0x00, H1_512_BLOCK_SIZE * 2 - LastByte - 9);
    databitlen = H1_512_BLOCK_SIZE * 16;
    M64[31] = state->bits_processed + state->unprocessed_bits;
  }

  H512 = hashState512(state)->DoublePipe;
  while (databitlen >= H1_512_BLOCK_SIZE * 8)
  {
    databitlen -= H1_512_BLOCK_SIZE * 8;
    Compression512(M64, H512);
    M64 += 16;
  }

  Compression512(H512, CONST64final);

  memcpy(hashval, CONST64final + 10, H1_384_DIGEST_SIZE);
  return (SUCCESS);
}