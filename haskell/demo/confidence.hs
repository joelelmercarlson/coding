#!/usr/bin/env stack
-- stack script --system-ghc --resolver lts-13.15 --package "aeson" --package "bytestring" --package "text"
{-# LANGUAGE DeriveAnyClass, DeriveGeneric, OverloadedStrings #-}
module Main where
  import System.Environment
  import System.Exit
  import System.IO

  import Data.Aeson
  import qualified Data.ByteString.Lazy.Char8 as L8
  import Data.Function (on)
  import Data.List
  import GHC.Generics
  import Text.Printf

  data Capabilities = Capabilities {
    list :: [Capability]
  } deriving (Show, Generic, FromJSON)

  data Capability = Capability {
    name          :: String
    , description :: String
    , capex       :: Float
    , opex        :: Float
    , novel       :: Float
    , season      :: Float
  } deriving (Show, Generic, FromJSON)

  answer :: Float -> String
  answer x = y
    where
      y
        | x >= 0.75 = "Yes"
        | x >= 0.50 = "Maybe Yes"
        | x >= 0.25 = "Maybe No"
        | otherwise = "No"

  banner :: IO ()
  banner = do
    printf "| Capability | Description | Percentage of Success 0-100 |\n"
    printf "|----|----|----|\n"

  confidence :: [Float] -> Float
  confidence [] = 1
  confidence x  = 100 * sum x / fromIntegral (length x)

  definition :: String -> String
  definition x = case x of
    "Capex"  -> "Do we have enough Funding?"
    "Opex"   -> "Do we have enough People?"
    "Novel"  -> "Do we know What to do?"
    "Season" -> "Do we have enough Time?"
    _        -> "Unknown"

  detail :: [(String, Float)] -> IO ()
  detail []         = return ()
  detail ((a,b):xs) = do
    printf "|  | %s %s | %s is %.2f |\n" (definition a) (answer b) a b
    detail xs

  display :: [Capability] -> IO ()
  display []     = return ()
  display (x:xs) = do
    display' x
    display xs

  display' :: Capability -> IO ()
  display' x   = do
    let ranks  = scoresToList x
        scores = [ y | (a,b) <- ranks, let y = fudge b ]
        total  = confidence scores
    printf "| %s | %s | Score = %0.4f |\n" (name x) (description x) total
    detail ranks

  fudge :: Float -> Float
  fudge x = y
    where
      y
        | x > 0.999 = 0.999
        | x < 0.001 = 0.001
        | otherwise = x

  loadSource :: FilePath -> IO (Either String Capabilities)
  loadSource x = do
    d <- eitherDecode <$> L8.readFile x
    return $ case d of
      Left err -> Left err
      Right xs -> Right xs

  percent :: Float -> Float
  percent x = (1 - x) * 100

  fstSort :: Ord a => [(a, b)] -> [(a, b)]
  fstSort = sortBy (flip compare `on` fst)

  sndSort :: Ord b => [(a, b)] -> [(a, b)]
  sndSort = sortBy (flip compare `on` snd)

  scoresToList :: Capability -> [(String, Float)]
  scoresToList x = [ ("Capex", capex x), ("Opex", opex x), ("Novel", novel x), ("Season", season x) ]

  main :: IO ()
  main = do
    d <- loadSource ("data/" ++ "capabilities.json")
    case d of
      Left err -> putStrLn err
      Right xs -> do
                    banner
                    display (list xs)

  -- | test data
  capability :: [(String, Float)]
  capability = [ ("Capex", 1.0), ("Opex", 1.0), ("Novel", 0.25), ("Season", 0.5) ]

  test :: Capability
  test = Capability {
    name          = "C12345"
    , description = "Contingency"
    , capex = 1.0
    , opex = 1.0
    , novel = 0.25
    , season = 0.5
  }
