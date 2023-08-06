/**
 * @file Afseal.cpp
 * --------------------------------------------------------------------
 * @brief Afseal is a C++ library that creates an abstraction over the basic
 *  functionalities of HElib as a Homomorphic Encryption library, such as
 *  addition, multiplication, scalar product and others.
 *
 *  This is the implementation file. Refer to the .h file for a well
 *  documented API ready to use.
 *  --------------------------------------------------------------------
 * @author Alberto Ibarrondo (ibarrond)
 *  --------------------------------------------------------------------
  * @bugs No known bugs
 */

/*  License: GNU GPL v3
 *
 *  Afseal is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  Pyfhel is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *  --------------------------------------------------------------------
 */

#include <math.h>       /* pow */
#include <fstream>      /* file management */
#include <assert.h>     /* assert */

#include "Afseal.h"


// ----------------------------- CLASS MANAGEMENT -----------------------------
Afseal::Afseal() {}

Afseal::Afseal(const Afseal &otherAfseal) {
  this->context = make_shared<SEALContext>(otherAfseal.context->first_context_data()->parms());

  //TODO: Copy Encoder ptr

  this->keyGenObj = make_shared<KeyGenerator>(*(this->context));
  this->secretKey = make_shared<SecretKey>(*(otherAfseal.secretKey));
  this->publicKey = make_shared<PublicKey>(*(otherAfseal.publicKey));
  this->relinKey = make_shared<RelinKeys>(*(otherAfseal.relinKey));
  this->rotateKeys = make_shared<GaloisKeys>(*(otherAfseal.rotateKeys));

  this->encryptor = make_shared<Encryptor>(*context, *publicKey, *secretKey);
  this->evaluator = make_shared<Evaluator>(*context);
  this->decryptor = make_shared<Decryptor>(*context, *secretKey);

  this->ckksEncoder = make_shared<CKKSEncoder>(*context);

  this->m = otherAfseal.m;
  this->base = otherAfseal.base;
  this->sec = otherAfseal.sec;
  this->intDigits = otherAfseal.intDigits;
  this->fracDigits = otherAfseal.fracDigits;
  this->flagBatch = otherAfseal.flagBatch;

  this->pool = otherAfseal.pool;
}

Afseal::~Afseal() {}

// ------------------------------ CRYPTOGRAPHY --------------------------------
// CONTEXT GENERATION
void Afseal::ContextGen(long m,
                        bool flagBatching,
                        long base,
                        long sec,
                        int intDigits,
                        int fracDigits,
                        std::vector<int> qs) {

  EncryptionParameters parms(scheme_type::ckks);
  this->m = m;
  this->base = base;
  this->sec = sec;
  this->intDigits = intDigits;
  this->fracDigits = fracDigits;
  this->flagBatch = flagBatching;

  // Context generation
  parms.set_poly_modulus_degree(m);
  parms.set_coeff_modulus(CoeffModulus::Create(m, qs));
  this->context = make_shared<SEALContext>(parms);

  // Create Evaluator Key
  this->evaluator = make_shared<Evaluator>(*context);
  this->ckksEncoder = make_shared<CKKSEncoder>(*context);

}

// KEY GENERATION
void Afseal::KeyGen() {
  if (context==NULL) { throw std::logic_error("Context not initialized"); }

  this->keyGenObj = make_shared<KeyGenerator>(*context);
  this->publicKey = make_shared<PublicKey>();// Extract keys
  keyGenObj->create_public_key(*publicKey);
  this->secretKey = make_shared<SecretKey>(keyGenObj->secret_key());

  this->encryptor = make_shared<Encryptor>(*context, *publicKey); // encr/decr objects
  this->decryptor = make_shared<Decryptor>(*context, *secretKey);
}

// ENCRYPTION
Ciphertext Afseal::encrypt(Plaintext &plain1) {
  if (encryptor==NULL) { throw std::logic_error("Missing a Public Key"); }
  Ciphertext cipher1;
  encryptor->encrypt(plain1, cipher1);
  return cipher1;
}

void Afseal::encrypt(Plaintext &plain1, Ciphertext &cipher1) {
  if (encryptor==NULL) { throw std::logic_error("Missing a Public Key"); }
  encryptor->encrypt(plain1, cipher1);
}

//DECRYPTION
Plaintext Afseal::decrypt(Ciphertext &cipher1) {
  if (decryptor==NULL) { throw std::logic_error("Missing a Private Key"); }
  Plaintext plain1;
  decryptor->decrypt(cipher1, plain1);
  return plain1;
}

void Afseal::decrypt(Ciphertext &cipher1, Plaintext &plainOut) {
  if (decryptor==NULL) { throw std::logic_error("Missing a Private Key"); }
  decryptor->decrypt(cipher1, plainOut);
}

// ---------------------------------- CODEC -----------------------------------
// ENCODE
Plaintext Afseal::encode(double &value1, double scale) {
  Plaintext ptxt;
  ckksEncoder->encode(value1, scale, ptxt);
  return ptxt;
}
Plaintext Afseal::encode(vector<double> &values, double scale) {
  Plaintext ptxt;
  ckksEncoder->encode(values, scale, ptxt);
  return ptxt;
}
Plaintext Afseal::encode(vector<std::complex<double>> &values, double scale) {
  Plaintext ptxt;
  ckksEncoder->encode(values, scale, ptxt);
  return ptxt;
}

void Afseal::encode(double &value1, double scale, Plaintext &plainOut) {
  ckksEncoder->encode(value1, scale, plainOut);
}

void Afseal::encode(vector<double> &values, double scale, Plaintext &plainOut) {
  ckksEncoder->encode(values, scale, plainOut);
}

void Afseal::encode(vector<complex<double>> &values, double scale, Plaintext &plainOut) {
  ckksEncoder->encode(values, scale, plainOut);
}

// DECODE
vector<double> Afseal::decode(Plaintext &plain1) {
  if (ckksEncoder==NULL) { throw std::logic_error("Context not initialized with BATCH support"); }
  vector<double> valueVOut;
  ckksEncoder->decode(plain1, valueVOut);
  return valueVOut;
}
void Afseal::decode(Plaintext &plain1, int64_t &valueOut) {
  throw std::logic_error("Non-Batched Integer Encoding no longer supported");
}
void Afseal::decode(Plaintext &plain1, vector<double> &valueVOut) {
  if (ckksEncoder==NULL) { throw std::logic_error("Context not initialized with BATCH support"); }
  ckksEncoder->decode(plain1, valueVOut);
}
void Afseal::decode(Plaintext &plain1, vector<std::complex<double>> &valueVOut) {
  if (ckksEncoder==NULL) { throw std::logic_error("Context not initialized with BATCH support"); }
  ckksEncoder->decode(plain1, valueVOut);
}
void Afseal::decode(vector<Plaintext> &plainV, vector<int64_t> &valueVOut) {
  throw std::logic_error("Non-Batched Integer Encoding no longer supported");
}
void Afseal::data(Ciphertext &ctxt, int index, uint64_t *dest) {
  dest = ctxt.data(index);
}

void Afseal::data(Plaintext &ptxt, uint64_t *dest) {
  dest = ptxt.data();
}

void Afseal::allocate_zero_poly(uint64_t n, uint64_t coeff_mod_count, uint64_t *dest) {
  dest = &util::allocate_zero_poly(n, coeff_mod_count, pool)[0];
}
// NOISE MEASUREMENT
int Afseal::noiseLevel(Ciphertext &cipher1) {
  if (decryptor==NULL) { throw std::logic_error("Missing a Private Key"); }
  return decryptor->invariant_noise_budget(cipher1);
}

// ------------------------------ RELINEARIZATION -----------------------------
void Afseal::relinKeyGen() {
  this->relinKey = std::make_shared<RelinKeys>();
  keyGenObj->create_relin_keys(*relinKey);
}
void Afseal::relinearize(Ciphertext &cipher1) {
  if (evaluator==NULL) { throw std::logic_error("Context not initialized"); }
  if (relinKey==NULL) { throw std::logic_error("Relinearization key not initialized"); }
  evaluator->relinearize_inplace(cipher1, *relinKey);
}
void Afseal::rotateKeyGen(int &bitCount) {
  if (keyGenObj==NULL) { throw std::logic_error("Context not initialized"); }
  if (bitCount > 60) { throw invalid_argument("bitCount must be =< 60"); }
  if (bitCount < 1) { throw invalid_argument("bitCount must be >= 1"); }
  rotateKeys = make_shared<GaloisKeys>();
  keyGenObj->create_galois_keys(*rotateKeys);
}

// --------------------------------- OPERATIONS -------------------------------
// NOT
void Afseal::negate(Ciphertext &cipher1) {
  if (evaluator==NULL) { throw std::logic_error("Context not initialized"); }
  evaluator->negate_inplace(cipher1);
}
void Afseal::negate(vector<Ciphertext> &cipherV) {
  if (evaluator==NULL) { throw std::logic_error("Context not initialized"); }
  for (Ciphertext &c:cipherV) { evaluator->negate_inplace(c); }
}
void Afseal::rescale_to_next(Ciphertext &cipher1) {
  if (evaluator==NULL) { throw std::logic_error("Context not initialized"); }
  evaluator->rescale_to_next_inplace(cipher1);
}

void Afseal::mod_switch_to_next(Ciphertext &cipher1) {
  if (evaluator==NULL) { throw std::logic_error("Context not initialized"); }
  evaluator->mod_switch_to_next_inplace(cipher1);
}

void Afseal::mod_switch_to_next(Plaintext &ptxt) {
  if (evaluator==NULL) { throw std::logic_error("Context not initialized"); }
  evaluator->mod_switch_to_next_inplace(ptxt);
}

// SQUARE
void Afseal::square(Ciphertext &cipher1) {
  if (evaluator==NULL) { throw std::logic_error("Context not initialized"); }
  evaluator->square_inplace(cipher1);
}
void Afseal::square(vector<Ciphertext> &cipherV) {
  if (evaluator==NULL) { throw std::logic_error("Context not initialized"); }
  for (Ciphertext &c:cipherV) { evaluator->square_inplace(c); }
}

// ADDITION
void Afseal::add(Ciphertext &cipherInOut, Ciphertext &cipher2) {
  if (evaluator==NULL) { throw std::logic_error("Context not initialized"); }
  evaluator->add_inplace(cipherInOut, cipher2);
}
void Afseal::add(Ciphertext &cipherInOut, Plaintext &plain2) {
  if (evaluator==NULL) { throw std::logic_error("Context not initialized"); }
  evaluator->add_plain_inplace(cipherInOut, plain2);
}
void Afseal::add(vector<Ciphertext> &cipherVInOut, vector<Ciphertext> &cipherV2) {
  if (evaluator==NULL) { throw std::logic_error("Context not initialized"); }
  vector<Ciphertext>::iterator c1 = cipherVInOut.begin();
  vector<Ciphertext>::iterator c2 = cipherV2.begin();
  for (; c1!=cipherVInOut.end(), c2!=cipherV2.end(); c1++, c2++) {
    evaluator->add_inplace(*c1, *c2);
  }
}
void Afseal::add(vector<Ciphertext> &cipherVInOut, vector<Plaintext> &plainV2) {
  if (evaluator==NULL) { throw std::logic_error("Context not initialized"); }
  vector<Ciphertext>::iterator c1 = cipherVInOut.begin();
  vector<Plaintext>::iterator p2 = plainV2.begin();
  for (; c1!=cipherVInOut.end(), p2!=plainV2.end(); c1++, p2++) {
    evaluator->add_plain_inplace(*c1, *p2);
  }
}
void Afseal::add(vector<Ciphertext> &cipherV, Ciphertext &cipherOut) {
  if (evaluator==NULL) { throw std::logic_error("Context not initialized"); }
  evaluator->add_many(cipherV, cipherOut);
}

// SUBSTRACTION
void Afseal::sub(Ciphertext &cipherInOut, Ciphertext &cipher2) {
  if (evaluator==NULL) { throw std::logic_error("Context not initialized"); }
  evaluator->sub_inplace(cipherInOut, cipher2);
}
void Afseal::sub(Ciphertext &cipherInOut, Plaintext &plain2) {
  if (evaluator==NULL) { throw std::logic_error("Context not initialized"); }
  evaluator->sub_plain_inplace(cipherInOut, plain2);
}
void Afseal::sub(vector<Ciphertext> &cipherVInOut, vector<Ciphertext> &cipherV2) {
  if (evaluator==NULL) { throw std::logic_error("Context not initialized"); }
  vector<Ciphertext>::iterator c1 = cipherVInOut.begin();
  vector<Ciphertext>::iterator c2 = cipherV2.begin();
  for (; c1!=cipherVInOut.end(), c2!=cipherV2.end(); c1++, c2++) {
    evaluator->sub_inplace(*c1, *c2);
  }
}
void Afseal::sub(vector<Ciphertext> &cipherVInOut, vector<Plaintext> &plainV2) {
  if (evaluator==NULL) { throw std::logic_error("Context not initialized"); }
  vector<Ciphertext>::iterator c1 = cipherVInOut.begin();
  vector<Plaintext>::iterator p2 = plainV2.begin();
  for (; c1!=cipherVInOut.end(), p2!=plainV2.end(); c1++, p2++) {
    evaluator->sub_plain_inplace(*c1, *p2);
  }
}

// MULTIPLICATION
void Afseal::multiply(Ciphertext &cipherInOut, Ciphertext &cipher2) {
  if (evaluator==NULL) { throw std::logic_error("Context not initialized"); }
  evaluator->multiply_inplace(cipherInOut, cipher2);
}
void Afseal::multiply(Ciphertext &cipherInOut, Plaintext &plain1) {
  if (evaluator==NULL) { throw std::logic_error("Context not initialized"); }
  evaluator->multiply_plain_inplace(cipherInOut, plain1);
}
void Afseal::multiply(vector<Ciphertext> &cipherVInOut, vector<Ciphertext> &cipherV2) {
  if (evaluator==NULL) { throw std::logic_error("Context not initialized"); }
  vector<Ciphertext>::iterator c1 = cipherVInOut.begin();
  vector<Ciphertext>::iterator c2 = cipherV2.begin();
  for (; c1!=cipherVInOut.end(), c2!=cipherV2.end(); c1++, c2++) {
    evaluator->multiply_inplace(*c1, *c2);
  }
}
void Afseal::multiply(vector<Ciphertext> &cipherVInOut, vector<Plaintext> &plainV2) {
  if (evaluator==NULL) { throw std::logic_error("Context not initialized"); }
  vector<Ciphertext>::iterator c1 = cipherVInOut.begin();
  vector<Plaintext>::iterator p2 = plainV2.begin();
  for (; c1!=cipherVInOut.end(), p2!=plainV2.end(); c1++, p2++) {
    evaluator->multiply_plain_inplace(*c1, *p2);
  }
}
void Afseal::multiply(vector<Ciphertext> &cipherV, Ciphertext &cipherOut) {
  if (evaluator==NULL) { throw std::logic_error("Context not initialized"); }
  if (relinKey==NULL) { throw std::logic_error("Relinearization key not initialized"); }
  evaluator->multiply_many(cipherV, *relinKey, cipherOut);
}

// ROTATION
void Afseal::rotate(Ciphertext &cipher1, int &k) {
  if (rotateKeys==NULL) { throw std::logic_error("Rotation keys not initialized"); }
  if (evaluator==NULL) { throw std::logic_error("Context not initialized"); }
  evaluator->rotate_vector_inplace(cipher1, k, *rotateKeys);
}
void Afseal::rotate(vector<Ciphertext> &cipherV, int &k) {
  if (rotateKeys==NULL) { throw std::logic_error("Rotation keys not initialized"); }
  if (evaluator==NULL) { throw std::logic_error("Context not initialized"); }
  for (Ciphertext &c:cipherV) { evaluator->rotate_vector_inplace(c, k, *rotateKeys); }
}

// POLYNOMIALS
void Afseal::exponentiate(Ciphertext &cipher1, uint64_t &expon) {
  if (relinKey==NULL) { throw std::logic_error("Relinearization key not initialized"); }
  if (evaluator==NULL) { throw std::logic_error("Context not initialized"); }
  evaluator->exponentiate_inplace(cipher1, expon, *relinKey);
}
void Afseal::exponentiate(vector<Ciphertext> &cipherV, uint64_t &expon) {
  if (relinKey==NULL) { throw std::logic_error("Relinearization key not initialized"); }
  if (evaluator==NULL) { throw std::logic_error("Context not initialized"); }
  for (Ciphertext &c:cipherV) { evaluator->exponentiate_inplace(c, expon, *relinKey); }
}

void Afseal::polyEval(Ciphertext &cipher1, vector<int64_t> &coeffPoly) {
  throw std::logic_error("Non-Batched Integer Encoder no longer supported");
}

void Afseal::polyEval(Ciphertext &cipher1, vector<double> &coeffPoly) {
  throw std::logic_error("Fractional Encoder no longer supported");
}

// ------------------------------------- I/O ----------------------------------
// SAVE/RESTORE CONTEXT
bool Afseal::saveContext(string fileName) {
  if (context==NULL) { throw std::logic_error("Context not initialized"); }
  bool res = true;
  try {
    fstream contextFile(fileName, fstream::out | fstream::trunc | fstream::binary);
    assert(contextFile.is_open());
    context->first_context_data()->parms().save(contextFile);
    contextFile << base << endl;
    contextFile << sec << endl;
    contextFile << intDigits << endl;
    contextFile << fracDigits << endl;
    contextFile << flagBatch << endl;

    contextFile.close();
  }
  catch (exception &e) {
    std::cout << "Afseal ERROR: context could not be saved";
    res = false;
  }
  return res;                                 // 1 if all OK, 0 otherwise
}

bool Afseal::restoreContext(string fileName) {
  EncryptionParameters parms(scheme_type::bfv);
  bool res = true;
  try {
    fstream contextFile(fileName, fstream::in | fstream::binary);
    assert(contextFile.is_open());
    parms.load(contextFile);
    contextFile >> base;
    contextFile >> sec;
    contextFile >> intDigits;
    contextFile >> fracDigits;
    contextFile >> flagBatch;
    contextFile.close();

    this->context = make_shared<SEALContext>(parms);
    this->keyGenObj = make_shared<KeyGenerator>(*context);
    //TODO: Initialize Encoder
    this->evaluator = make_shared<Evaluator>(*context);
    if (flagBatch) {
      if (!(*context).first_context_data()->qualifiers().using_batching) {
        throw invalid_argument("p not prime | p-1 not multiple 2*m");
      }
      this->flagBatch = true;
      this->ckksEncoder = make_shared<CKKSEncoder>(*context);
    }
  }
  catch (exception &e) {
    std::cout << "Afseal ERROR: context could not be loaded";
    res = false;
  }
  return res;                                 // 1 if all OK, 0 otherwise
}

// SAVE/RESTORE KEYS
bool Afseal::savepublicKey(string fileName) {
  if (publicKey==NULL) { throw std::logic_error("Public Key not initialized"); }
  bool res = true;
  try {
    fstream keyFile(fileName, fstream::out | fstream::trunc | fstream::binary);
    assert(keyFile.is_open());
    publicKey->save(keyFile);

    keyFile.close();
  }
  catch (exception &e) {
    std::cout << "Afseal ERROR: public key could not be saved";
    res = false;
  }
  return res;                                 // 1 if all OK, 0 otherwise
}

bool Afseal::restorepublicKey(string fileName) {
  throw std::logic_error("Serialization Support Removed Temporarily");
  //TODO: Add Serialization support
  //  bool res = true;
  //  try {
  //    fstream keyFile(fileName, fstream::in | fstream::binary);
  //    assert(keyFile.is_open());
  //    this->publicKey = make_shared<PublicKey>();
  //    this->publicKey->load(context, keyFile);
  //    this->encryptor = make_shared<Encryptor>(*context, *publicKey);
  //    keyFile.close();
  //  }
  //  catch (exception &e) {
  //    std::cout << "Afseal ERROR: public key could not be loaded";
  //    res = false;
  //  }
  //  return res;                                 // 1 if all OK, 0 otherwise
}

bool Afseal::savesecretKey(string fileName) {
  throw std::logic_error("Serialization Support Removed Temporarily");
  //TODO: Add Serialization support
  //  if (publicKey==NULL) { throw std::logic_error("Secret Key not initialized"); }
  //  bool res = true;
  //  try {
  //    fstream keyFile(fileName, fstream::out | fstream::trunc | fstream::binary);
  //    assert(keyFile.is_open());
  //    secretKey->save(keyFile);
  //
  //    keyFile.close();
  //  }
  //  catch (exception &e) {
  //    std::cout << "Afseal ERROR: secret key could not be saved";
  //    res = false;
  //  }
  //  return res;                                 // 1 if all OK, 0 otherwise
}

bool Afseal::restoresecretKey(string fileName) {
  throw std::logic_error("Serialization Support Removed Temporarily");
  //TODO: Add Serialization support
  //  bool res = true;
  //  try {
  //    fstream keyFile(fileName, fstream::in | fstream::binary);
  //    assert(keyFile.is_open());
  //    this->secretKey = make_shared<SecretKey>();
  //    this->secretKey->load(context, keyFile);
  //    this->decryptor = make_shared<Decryptor>(*context, *secretKey);
  //    keyFile.close();
  //  }
  //  catch (exception &e) {
  //    std::cout << "Afseal ERROR: secret key could not be saved";
  //    res = false;
  //  }
  //  return res;                                 // 1 if all OK, 0 otherwise
}

bool Afseal::saverelinKey(string fileName) {
  throw std::logic_error("Serialization Support Removed Temporarily");
  //TODO: Add Serialization support
  //  if (relinKey==NULL) { throw std::logic_error("Relinearization Key not initialized"); }
  //  bool res = true;
  //  try {
  //    fstream keyFile(fileName, fstream::out | fstream::trunc | fstream::binary);
  //    assert(keyFile.is_open());
  //    relinKey->save(keyFile);
  //
  //    keyFile.close();
  //  }
  //  catch (exception &e) {
  //    std::cout << "Afseal ERROR: relinearization key could not be saved";
  //    res = false;
  //  }
  //  return res;                                 // 1 if all OK, 0 otherwise
}

bool Afseal::restorerelinKey(string fileName) {
  throw std::logic_error("Serialization Support Removed Temporarily");
  //TODO: Add Serialization support
  //  bool res = true;
  //  try {
  //    fstream keyFile(fileName, fstream::in | fstream::binary);
  //    assert(keyFile.is_open());
  //    this->relinKey = make_shared<RelinKeys>();
  //    this->relinKey->load(context, keyFile);
  //    keyFile.close();
  //  }
  //  catch (exception &e) {
  //    std::cout << "Afseal ERROR: relinearization key could not be loaded";
  //    res = false;
  //  }
  //  return res;                                 // 1 if all OK, 0 otherwise
}

bool Afseal::saverotateKey(string fileName) {
  throw std::logic_error("Serialization Support Removed Temporarily");
  //TODO: Add Serialization support
  //  if (rotateKeys==NULL) { throw std::logic_error("Rotation Key not initialized"); }
  //  bool res = true;
  //  try {
  //    fstream keyFile(fileName, fstream::out | fstream::trunc | fstream::binary);
  //    assert(keyFile.is_open());
  //    rotateKeys->save(keyFile);
  //
  //    keyFile.close();
  //  }
  //  catch (exception &e) {
  //    std::cout << "Afseal ERROR: Galois could not be saved";
  //    res = false;
  //  }
  //  return res;                                 // 1 if all OK, 0 otherwise
}

bool Afseal::restorerotateKey(string fileName) {
  throw std::logic_error("Serialization Support Removed Temporarily");
  //TODO: Add Serialization support
  //  bool res = true;
  //  try {
  //    fstream keyFile(fileName, fstream::in | fstream::binary);
  //    assert(keyFile.is_open());
  //    this->rotateKeys = make_shared<GaloisKeys>();
  //    this->rotateKeys->load(context, keyFile);
  //    keyFile.close();
  //  }
  //  catch (exception &e) {
  //    std::cout << "Afseal ERROR: Galois could not be loaded";
  //    res = false;
  //  }
  //  return res;                                 // 1 if all OK, 0 otherwise
}

// ++++ FROM STREAMS ++++
// SAVE/RESTORE CONTEXT
bool Afseal::ssaveContext(ostream &contextFile) {
  throw std::logic_error("Serialization Support Removed Temporarily");
  //TODO: Add Serialization support
//  if(context==NULL){throw std::logic_error("Context not initialized");}
//  bool res=true;
//  try{
//    context->parms().save(contextFile);
//    contextFile << base << endl;
//    contextFile << sec << endl;
//    contextFile << intDigits << endl;
//    contextFile << fracDigits << endl;
//    contextFile << flagBatch << endl;
//  }
//  catch(exception& e){
//    std::cout << "Afseal ERROR: context could not be saved";
//    res=false;
//  }
//  return res;                                 // 1 if all OK, 0 otherwise
}

bool Afseal::srestoreContext(istream &contextFile) {
  throw std::logic_error("Serialization Support Removed Temporarily");
  //TODO: Add Serialization support
//  EncryptionParameters parms;
//  bool res=true;
//  try{
//    parms.load(contextFile);
//    contextFile >> base;
//    contextFile >> sec;
//    contextFile >> intDigits;
//    contextFile >> fracDigits;
//    contextFile >> flagBatch;
//
//    this->context = make_shared<SEALContext>(parms);
//    this->keyGenObj = make_shared<KeyGenerator>(*context);
//    this->intEncoder = make_shared<IntegerEncoder>((*context).plain_modulus(), base);
//    this->fracEncoder = make_shared<FractionalEncoder>((*context).plain_modulus(),
//                                                       (*context).poly_modulus(), intDigits, fracDigits, base);
//    this->evaluator=make_shared<Evaluator>(*context);
//    if(flagBatch){
//      if(!(*context).qualifiers().enable_batching){
//        throw invalid_argument("p not prime | p-1 not multiple 2*m");
//      }
//      this->flagBatch=true;
//      this->crtBuilder=make_shared<PolyCRTBuilder>(*context);
//    }
//  }
//  catch(exception& e){
//    std::cout << "Afseal ERROR: context could not be loaded";
//    res=false;
//  }
//  return res;                                 // 1 if all OK, 0 otherwise
}

// SAVE/RESTORE KEYS
bool Afseal::ssavepublicKey(ostream &keyFile) {
  throw std::logic_error("Serialization Support Removed Temporarily");
  //TODO: Add Serialization support
//  if(publicKey==NULL){throw std::logic_error("Public Key not initialized");}
//  bool res=true;
//  try{
//    publicKey->save(keyFile);
//  }
//  catch(exception& e){
//    std::cout << "Afseal ERROR: public key could not be saved";
//    res=false;
//  }
//  return res;                                 // 1 if all OK, 0 otherwise
}

bool Afseal::srestorepublicKey(istream &keyFile) {
  throw std::logic_error("Serialization Support Removed Temporarily");
  //TODO: Add Serialization support
//  bool res=true;
//  try{
//    this->publicKey = make_shared<PublicKey>();
//    this->publicKey->load(keyFile);
//    this->encryptor=make_shared<Encryptor>(*context, *publicKey);
//  }
//  catch(exception& e){
//    std::cout << "Afseal ERROR: public key could not be loaded";
//    res=false;
//  }
//  return res;                                 // 1 if all OK, 0 otherwise
}

bool Afseal::ssavesecretKey(ostream &keyFile) {
  throw std::logic_error("Serialization Support Removed Temporarily");
  //TODO: Add Serialization support
//  if(publicKey==NULL){throw std::logic_error("Secret Key not initialized");}
//  bool res=true;
//  try{
//    secretKey->save(keyFile);
//  }
//  catch(exception& e){
//    std::cout << "Afseal ERROR: secret key could not be saved";
//    res=false;
//  }
//  return res;                                 // 1 if all OK, 0 otherwise
}

bool Afseal::srestoresecretKey(istream &keyFile) {
  throw std::logic_error("Serialization Support Removed Temporarily");
  //TODO: Add Serialization support
//  bool res=true;
//  try{
//    this->secretKey = make_shared<SecretKey>();
//    this->secretKey->load(keyFile);
//    this->decryptor=make_shared<Decryptor>(*context, *secretKey);
//  }
//  catch(exception& e){
//    std::cout << "Afseal ERROR: secret key could not be saved";
//    res=false;
//  }
//  return res;                                 // 1 if all OK, 0 otherwise
}

bool Afseal::ssaverelinKey(ostream &keyFile) {
  throw std::logic_error("Serialization Support Removed Temporarily");
  //TODO: Add Serialization support
//  if(relinKey==NULL){throw std::logic_error("Relinearization Key not initialized");}
//  bool res=true;
//  try{
//    relinKey->save(keyFile);
//  }
//  catch(exception& e){
//    std::cout << "Afseal ERROR: relinearization key could not be saved";
//    res=false;
//  }
//  return res;                                 // 1 if all OK, 0 otherwise
}

bool Afseal::srestorerelinKey(istream &keyFile) {
  throw std::logic_error("Serialization Support Removed Temporarily");
  //TODO: Add Serialization support
//  bool res=true;
//  try{
//    this->relinKey = make_shared<EvaluationKeys>();
//    this->relinKey->load(keyFile);
//  }
//  catch(exception& e){
//    std::cout << "Afseal ERROR: relinearization key could not be loaded";
//    res=false;
//  }
//  return res;                                 // 1 if all OK, 0 otherwise
}

bool Afseal::ssaverotateKey(ostream &keyFile) {
  throw std::logic_error("Serialization Support Removed Temporarily");
  //TODO: Add Serialization support
//  if(rotateKeys==NULL){throw std::logic_error("Rotation Key not initialized");}
//  bool res=true;
//  try{
//    rotateKeys->save(keyFile);
//  }
//  catch(exception& e){
//    std::cout << "Afseal ERROR: Galois could not be saved";
//    res=false;
//  }
//  return res;                                 // 1 if all OK, 0 otherwise
}

bool Afseal::srestorerotateKey(istream &keyFile) {
  throw std::logic_error("Serialization Support Removed Temporarily");
  //TODO: Add Serialization support
//  bool res=true;
//  try{
//    this->rotateKeys = make_shared<GaloisKeys>();
//    this->rotateKeys->load(keyFile);
//  }
//  catch(exception& e){
//    std::cout << "Afseal ERROR: Galois could not be loaded";
//    res=false;
//  }
//  return res;                                 // 1 if all OK, 0 otherwise
}

// ----------------------------- AUXILIARY ----------------------------
bool Afseal::batchEnabled() {
  if (this->context==NULL) { throw std::logic_error("Context not initialized"); }
  return this->context->first_context_data()->qualifiers().using_batching;
}
long Afseal::relinBitCount() {
  throw std::logic_error("relinBitCount is potentially no longer exposed");
}
long Afseal::maxBitCount(long poly_modulus_degree, int sec_level) {
  auto
      s = sec_level <= 128 ? sec_level_type::tc128 : (sec_level >= 256 ? sec_level_type::tc256 : sec_level_type::tc256);
  return CoeffModulus::MaxBitCount(poly_modulus_degree, s);
}
double Afseal::scale(Ciphertext &ctxt) {
  return ctxt.scale();
}
void Afseal::override_scale(Ciphertext &ctxt, double scale) {
  ctxt.scale() = scale;
}
// GETTERS
SecretKey Afseal::getsecretKey() {
  if (this->secretKey==NULL) { throw std::logic_error("Secret Key not initialized"); }
  return *(this->secretKey);
}
PublicKey Afseal::getpublicKey() {
  if (this->publicKey==NULL) { throw std::logic_error("Public Key not initialized"); }
  return *(this->publicKey);
}
RelinKeys Afseal::getrelinKey() {
  if (this->relinKey==NULL) { throw std::logic_error("Relinearization Key not initialized"); }
  return *(this->relinKey);
}
GaloisKeys Afseal::getrotateKeys() {
  if (this->rotateKeys==NULL) { throw std::logic_error("Rotation Key not initialized"); }
  return *(this->rotateKeys);
}
int Afseal::getnSlots() {
  if (this->ckksEncoder==NULL) { throw std::logic_error("Context not initialized with BATCH support"); }
  return this->ckksEncoder->slot_count();
}
int Afseal::getm() {
  if (this->context==NULL) { throw std::logic_error("Context not initialized"); }
  return this->m;
}
int Afseal::getbase() {
  if (this->context==NULL) { throw std::logic_error("Context not initialized"); }
  return this->base;
}
int Afseal::getsec() {
  if (this->context==NULL) { throw std::logic_error("Context not initialized"); }
  return this->sec;
}
int Afseal::getintDigits() {
  if (this->context==NULL) { throw std::logic_error("Context not initialized"); }
  return this->intDigits;
}
int Afseal::getfracDigits() {
  if (this->context==NULL) { throw std::logic_error("Context not initialized"); }
  return this->fracDigits;
}
bool Afseal::getflagBatch() {
  if (this->context==NULL) { throw std::logic_error("Context not initialized"); }
  return this->flagBatch;
}
